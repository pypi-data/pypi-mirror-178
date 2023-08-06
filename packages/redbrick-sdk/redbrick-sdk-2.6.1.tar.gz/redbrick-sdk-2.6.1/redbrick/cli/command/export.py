"""CLI export command."""
import asyncio
import os
import re
from datetime import datetime, timezone
from argparse import ArgumentError, ArgumentParser, Namespace
from typing import List, Dict, Optional, Tuple
import shutil

import tqdm  # type: ignore

from redbrick.cli.project import CLIProject
from redbrick.cli.cli_base import CLIExportInterface
from redbrick.utils.files import uniquify_path, download_files
from redbrick.utils.logging import log_error, logger


class CLIExportController(CLIExportInterface):
    """CLI export command controller."""

    def __init__(self, parser: ArgumentParser) -> None:
        """Intialize export sub commands."""
        parser.add_argument(
            "type",
            nargs="?",
            default=self.TYPE_LATEST,
            help=f"Export type: ({self.TYPE_LATEST} [default], {self.TYPE_GROUNDTRUTH}, <task id>)",
        )
        parser.add_argument(
            "--with-files",
            action="store_true",
            help="Export with files (e.g. images/video frames)",
        )
        parser.add_argument(
            "--old-format",
            action="store_true",
            help="""Whether to export tasks in old format. (Default: False)""",
        )
        parser.add_argument(
            "--no-consensus",
            action="store_true",
            help="""Whether to export tasks without consensus info.
            If None, will default to export with consensus info,
            if it is enabled for the given project.""",
        )
        parser.add_argument(
            "--png", action="store_true", help="Export labels as png masks"
        )
        parser.add_argument(
            "--clear-cache", action="store_true", help="Clear local cache"
        )
        parser.add_argument(
            "--concurrency",
            "-c",
            type=int,
            default=10,
            help="Concurrency value (Default: 10)",
        )
        parser.add_argument(
            "--stage",
            "-s",
            help="Export tasks that are currently in the given stage. "
            + f"Applicable for only type = {self.TYPE_LATEST}",
        )
        parser.add_argument(
            "--destination",
            "-d",
            default=".",
            help="Destination directory (Default: current directory)",
        )

    def handler(self, args: Namespace) -> None:
        """Handle export command."""
        self.args = args
        project = CLIProject.from_path()
        assert project, "Not a valid project"
        self.project = project

        self.handle_export()

    def handle_export(self) -> None:
        """Handle empty sub command."""
        # pylint: disable=too-many-statements, too-many-locals, too-many-branches, protected-access
        if (
            self.args.type not in (self.TYPE_LATEST, self.TYPE_GROUNDTRUTH)
            and re.match(
                r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$",
                self.args.type.strip().lower(),
            )
            is None
        ):
            raise ArgumentError(None, "")

        if self.args.clear_cache:
            self.project.cache.clear_cache(True)

        no_consensus = (
            self.args.no_consensus
            if self.args.no_consensus
            else not self.project.project.consensus_enabled
        )

        cached_datapoints: Dict = {}
        cache_timestamp = None
        dp_conf = self.project.conf.get_section("datapoints")
        if dp_conf and "timestamp" in dp_conf:
            cached_dp = self.project.cache.get_data("datapoints", dp_conf["cache"])
            if isinstance(cached_dp, dict):
                cached_datapoints = cached_dp
                cache_timestamp = int(dp_conf["timestamp"]) or None

        current_timestamp = int(datetime.now(timezone.utc).timestamp())
        datapoints, taxonomy = self.project.project.export._get_raw_data_latest(
            self.args.concurrency,
            False,
            cache_timestamp,
            None,
            False,
            bool(self.project.project.label_stages)
            and not bool(self.project.project.review_stages)
            and not no_consensus,
        )

        logger.info(f"Refreshed {len(datapoints)} newly updated tasks")

        for datapoint in datapoints:
            cached_datapoints[datapoint["taskId"]] = datapoint

        dp_hash = self.project.cache.set_data("datapoints", cached_datapoints)
        self.project.conf.set_section(
            "datapoints",
            {
                "timestamp": str(
                    current_timestamp if datapoints else (cache_timestamp or 0)
                ),
                "cache": dp_hash,
            },
        )
        self.project.conf.save()

        data = list(cached_datapoints.values())

        if self.args.type == self.TYPE_LATEST:
            if self.args.stage:
                data = [
                    task
                    for task in data
                    if task["currentStageName"].lower() == self.args.stage.lower()
                ]
        elif self.args.type == self.TYPE_GROUNDTRUTH:
            data = [task for task in data if task["currentStageName"] == "END"]
        else:
            task_id = self.args.type.strip().lower()
            task = None
            for dpoint in data:
                if dpoint["taskId"] == task_id:
                    task = dpoint
                    break
            data = [task] if task else []

        loop = asyncio.get_event_loop()

        self.project.conf.save()

        export_dir = self.args.destination

        os.makedirs(export_dir, exist_ok=True)

        if self.args.with_files:
            try:
                loop.run_until_complete(self._download_files(data, export_dir))
            except Exception:  # pylint: disable=broad-except
                log_error("Failed to download files")

        png_mask = bool(self.args.png)
        nifti_dir = os.path.join(export_dir, "segmentations")
        os.makedirs(nifti_dir, exist_ok=True)
        task_map = os.path.join(export_dir, "tasks.json")
        class_map = os.path.join(export_dir, "class_map.json")
        self.project.project.export.export_nifti_label_data(
            data,
            taxonomy,
            nifti_dir,
            task_map,
            class_map,
            bool(self.args.old_format),
            no_consensus,
            png_mask,
        )
        logger.info(f"Exported: {task_map}")
        logger.info(f"Exported nifti to: {nifti_dir}")
        if png_mask:
            logger.info(f"Exported: {class_map}")

    async def _download_files(self, data: List[Dict], export_dir: str) -> None:
        # pylint: disable=too-many-locals
        parent_dir = os.path.join(export_dir, "tasks")
        os.makedirs(parent_dir, exist_ok=True)

        path_pattern = re.compile(r"[^\w.]+")

        files: List[Tuple[Optional[str], Optional[str]]] = []
        tasks_indices: List[List[int]] = []

        logger.info("Preparing to download files")
        for task in tqdm.tqdm(data):
            task_name = (
                re.sub(path_pattern, "-", task.get("name", "")) or task["taskId"]
            )
            task_dir = os.path.join(parent_dir, task_name)
            if os.path.isdir(task_dir):
                logger.info(f"{task_dir} exists. Skipping")
                continue
            shutil.rmtree(task_dir, ignore_errors=True)
            os.makedirs(task_dir, exist_ok=True)
            series_dirs: List[str] = []
            series_items_indices: List[List[int]] = []
            if sum(
                map(
                    lambda val: len(val.get("itemsIndices", []) or []) if val else 0,
                    task.get("seriesInfo", []) or [],
                )
            ) == len(task["items"]) and (
                len(task["seriesInfo"]) > 1 or task["seriesInfo"][0].get("name")
            ):
                for series_idx, series in enumerate(task["seriesInfo"]):
                    series_dir = uniquify_path(
                        os.path.join(
                            task_dir,
                            re.sub(path_pattern, "-", series.get("name", "") or "")
                            or chr(series_idx + ord("A")),
                        )
                    )
                    os.makedirs(series_dir)
                    series_dirs.append(series_dir)
                    series_items_indices.append(series["itemsIndices"])
            else:
                series_dir = os.path.join(task_dir, task_name)
                os.makedirs(series_dir)
                series_dirs.append(series_dir)
                series_items_indices.append(list(range(len(task["items"]))))

            to_presign = []
            local_files = []
            tasks_indices.append([])
            for series_dir, items_indices in zip(series_dirs, series_items_indices):
                paths = [task["items"][item_idx] for item_idx in items_indices]
                file_names = [
                    re.sub(path_pattern, "-", os.path.basename(path)) for path in paths
                ]
                fill_index = (
                    0
                    if all(file_names) and len(file_names) == len(set(file_names))
                    else len(str(len(file_names)))
                )
                to_presign.extend(paths)
                tasks_indices[-1].extend(items_indices)
                for index, item in enumerate(file_names):
                    file_name, file_ext = os.path.splitext(item)
                    local_files.append(
                        os.path.join(
                            series_dir,
                            file_name
                            + (
                                ("-" + str(index).zfill(fill_index))
                                if fill_index
                                else ""
                            )
                            + file_ext,
                        )
                    )

            presigned = self.project.context.export.presign_items(
                self.project.org_id, task["storageId"], to_presign
            )
            files.extend(list(zip(presigned, local_files)))

        downloaded = await download_files(files)
        task_idx = 0
        index_idx = 0
        for (url, _), file_path in zip(files, downloaded):
            data[task_idx]["items"][tasks_indices[task_idx][index_idx]] = (
                file_path or url
            )
            index_idx += 1
            if index_idx == len(tasks_indices[task_idx]):
                task_idx += 1
                index_idx = 0
