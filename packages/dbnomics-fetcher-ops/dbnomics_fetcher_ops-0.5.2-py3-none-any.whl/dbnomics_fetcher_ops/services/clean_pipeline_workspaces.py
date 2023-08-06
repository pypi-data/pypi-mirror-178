import shutil
from itertools import islice
from pathlib import Path
from typing import Iterator, Optional, cast

import daiquiri

from dbnomics_fetcher_ops.gitlab import init_gitlab_client
from dbnomics_fetcher_ops.model import FetcherDefNotFound, FetcherMetadata
from dbnomics_fetcher_ops.utils import iter_child_directories
from gitlab.v4.objects import Project, ProjectPipeline

logger = daiquiri.getLogger(__name__)

DEFAULT_KEEP_FAILED_COUNT = 3
DEFAULT_KEEP_SUCCESS_COUNT = 1


def clean_fetcher_workspace_pipeline_directories(
    workspace_dir: Path,
    *,
    debug_gitlab: bool = False,
    dry_run: bool = False,
    fetcher_metadata: FetcherMetadata,
    gitlab_private_token: Optional[str] = None,
    keep_failed_count: int = DEFAULT_KEEP_FAILED_COUNT,
    keep_success_count: int = DEFAULT_KEEP_SUCCESS_COUNT,
):
    provider_slug = workspace_dir.name

    try:
        fetcher_def = fetcher_metadata.find_fetcher_def_by_provider_slug(provider_slug)
    except FetcherDefNotFound:
        logger.warning("Skipping provider %r", provider_slug, exc_info=True)
        return

    provider_code = fetcher_def.provider_code

    gitlab_url = fetcher_metadata.gitlab.base_url
    gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

    project_path_with_namespace = fetcher_metadata.gitlab.fetcher.get_path_with_namespace(provider_slug)
    project = gl.projects.get(project_path_with_namespace)

    pipelines_to_keep = fetch_pipelines_to_keep(
        project,
        keep_failed_count=keep_failed_count,
        keep_success_count=keep_success_count,
    )
    logger.debug("Keeping pipeline directories of fetcher %r: %r", provider_code, pipelines_to_keep)

    for pipeline_dir in sorted(iter_child_directories(workspace_dir / "pipelines", warn_other=True)):
        clean_fetcher_workspace_pipeline_directory(pipeline_dir, dry_run=dry_run, pipelines_to_keep=pipelines_to_keep)


def clean_fetcher_workspace_pipeline_directory(
    pipeline_dir: Path, *, dry_run: bool = False, pipelines_to_keep: dict[str, list[int]]
):
    try:
        pipeline_id = int(pipeline_dir.name)
    except ValueError:
        logger.warning(
            "Ignoring sub-directory %r of workspace directory that does not seem to be a pipeline ID",
            str(pipeline_dir),
        )
        return

    if pipeline_id in pipelines_to_keep["running"]:
        logger.debug(
            "Keeping pipeline directory %r because the pipeline is running",
            str(pipeline_dir),
        )
        return

    if pipeline_id in pipelines_to_keep["success"]:
        logger.debug(
            "Keeping pipeline directory %r because the pipeline is one of the successful pipelines to keep",
            str(pipeline_dir),
        )
        return

    if pipeline_id in pipelines_to_keep["failed"]:
        logger.debug(
            "Keeping pipeline directory %r because the pipeline is one of the failed pipelines to keep",
            str(pipeline_dir),
        )
        return

    if dry_run:
        logger.info("[SKIPPED (dry-run)] The directory %r would have been deleted", str(pipeline_dir))
    else:
        shutil.rmtree(pipeline_dir)
        logger.info("The directory %r was deleted", str(pipeline_dir))


def fetch_pipelines_to_keep(
    project: Project, *, keep_failed_count: int, keep_success_count: int
) -> dict[str, list[int]]:
    pipelines_to_keep = {
        "failed": [
            pipeline.id for pipeline in islice(fetch_latest_pipelines(project, status="failed"), keep_failed_count)
        ],
        "running": [pipeline.id for pipeline in fetch_latest_pipelines(project, status="running")],
        "success": [
            pipeline.id for pipeline in islice(fetch_latest_pipelines(project, status="success"), keep_success_count)
        ],
    }
    return pipelines_to_keep


def fetch_latest_pipelines(project: Project, *, status: str) -> Iterator[ProjectPipeline]:
    return cast(
        Iterator[ProjectPipeline],
        project.pipelines.list(status=status, order_by="updated_at", sorted="desc", iterator=True),
    )
