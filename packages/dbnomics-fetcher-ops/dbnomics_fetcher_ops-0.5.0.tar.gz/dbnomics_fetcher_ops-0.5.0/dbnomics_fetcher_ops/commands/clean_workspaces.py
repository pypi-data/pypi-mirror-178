from pathlib import Path

import typer

from dbnomics_fetcher_ops.services.clean_pipeline_workspaces import (
    DEFAULT_KEEP_FAILED_COUNT,
    DEFAULT_KEEP_SUCCESS_COUNT,
    cleanup_fetcher_workspace_pipelines,
)
from dbnomics_fetcher_ops.utils import iter_child_directories


def clean_workspaces_command(
    workspaces_dir: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="Base directory where each child directory is the workspace of a fetcher",
    ),
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
    gitlab_url: str = typer.Option(..., envvar="GITLAB_URL", help="Base URL of GitLab instance"),
    gitlab_private_token: str = typer.Option(
        None,
        envvar="GITLAB_PRIVATE_TOKEN",
        help="Private access token used to authenticate to GitLab API",
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
    from ..app_args import app_args

    assert app_args is not None

    for fetcher_dir in iter_child_directories(workspaces_dir):
        cleanup_fetcher_workspace_pipelines(
            fetcher_dir,
            debug_gitlab=debug_gitlab,
            dry_run=app_args.dry_run,
            fetcher_metadata=app_args.fetcher_metadata,
            keep_failed_count=keep_failed_count,
            keep_success_count=keep_success_count,
            gitlab_url=gitlab_url,
            gitlab_private_token=gitlab_private_token,
        )
