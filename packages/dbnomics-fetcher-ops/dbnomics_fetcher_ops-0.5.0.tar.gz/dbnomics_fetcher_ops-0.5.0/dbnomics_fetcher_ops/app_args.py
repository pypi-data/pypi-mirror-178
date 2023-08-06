from dataclasses import dataclass
from typing import Optional

import typer

from .model import FetcherMetadata, PipelinesConfig

__all__ = ["app_args", "AppArgs", "check_provider_slug_is_lowercase", "get_fetcher_def_not_found_error_message"]

app_args: Optional["AppArgs"] = None


@dataclass
class AppArgs:
    """Script arguments common to all commands."""

    fetcher_metadata: FetcherMetadata
    fetchers_yml: str
    pipelines_config: PipelinesConfig
    pipelines_yml: str

    debug: bool = False
    dry_run: bool = False
    verbose: bool = False


def check_provider_slug_is_lowercase(value: str):
    if value != value.lower():
        raise typer.BadParameter("Provider slug must be lowercase")
    return value


def get_fetcher_def_not_found_error_message(provider_slug: str, fetchers_yml: str) -> str:
    return f"Could not find fetcher definition for provider {provider_slug!r} in {fetchers_yml!r}"
