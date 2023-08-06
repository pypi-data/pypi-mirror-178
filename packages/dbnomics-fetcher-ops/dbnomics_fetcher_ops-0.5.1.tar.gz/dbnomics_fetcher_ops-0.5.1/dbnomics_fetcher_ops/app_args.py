from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .model import FetcherMetadata, PipelinesConfig

__all__ = ["get_app_args", "AppArgs"]


def get_app_args() -> AppArgs:
    global _app_args
    if _app_args is None:
        # Cf "main_callback"
        raise ValueError("App args were not initialized")
    return _app_args


@dataclass
class AppArgs:
    """Script arguments common to all commands."""

    fetcher_metadata: FetcherMetadata
    fetchers_yml: str
    pipelines_config: PipelinesConfig
    pipelines_yml: str

    debug: bool = False
    debug_gitlab: bool = False
    dry_run: bool = False
    gitlab_private_token: Optional[str] = None
    verbose: bool = False


_app_args: Optional[AppArgs] = None
