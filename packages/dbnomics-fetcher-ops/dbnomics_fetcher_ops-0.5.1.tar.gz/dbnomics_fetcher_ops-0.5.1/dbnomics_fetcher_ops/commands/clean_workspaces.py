from pathlib import Path

import typer

from dbnomics_fetcher_ops.app_args import get_app_args
from dbnomics_fetcher_ops.services.clean_pipeline_workspaces import (
    DEFAULT_KEEP_FAILED_COUNT,
    DEFAULT_KEEP_SUCCESS_COUNT,
    clean_fetcher_workspace_pipeline_directories,
)
from dbnomics_fetcher_ops.utils import iter_child_directories


def clean_workspaces(
    workspaces_root_dir: Path = typer.Argument(
        ...,
        envvar="WORKSPACES_ROOT_DIR",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="Base directory where each child directory is the workspace of a fetcher",
    ),
    keep_failed_count: int = typer.Option(
        DEFAULT_KEEP_FAILED_COUNT,
        "--failed",
        help="keep this number of failed pipeline directories in workspace",
    ),
    keep_success_count: int = typer.Option(
        DEFAULT_KEEP_SUCCESS_COUNT,
        "--success",
        help="keep this number of success pipeline directories in workspace",
    ),
):
    """Cleanup the workspaces of DBnomics fetcher pipelines.

    Workspaces are directories where jobs of the fetcher pipeline store data while running.

    This CLI tool cleans those directories to avoid filling the disk by keeping the workspaces of
    the N latest failed jobs, and the M latest successful pipelines.
    """
    app_args = get_app_args()

    for workspace_dir in iter_child_directories(workspaces_root_dir):
        clean_fetcher_workspace_pipeline_directories(
            workspace_dir,
            debug_gitlab=app_args.debug_gitlab,
            dry_run=app_args.dry_run,
            fetcher_metadata=app_args.fetcher_metadata,
            keep_failed_count=keep_failed_count,
            keep_success_count=keep_success_count,
            gitlab_private_token=app_args.gitlab_private_token,
        )
