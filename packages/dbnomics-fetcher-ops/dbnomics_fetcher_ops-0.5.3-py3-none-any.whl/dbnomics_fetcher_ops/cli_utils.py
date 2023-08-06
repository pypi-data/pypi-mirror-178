from typer import BadParameter


def check_provider_slug_is_lowercase(value: str):
    if value != value.lower():
        raise BadParameter("Provider slug must be lowercase")
    return value


def get_fetcher_def_not_found_error_message(provider_slug: str, fetchers_yml: str) -> str:
    return f"Could not find fetcher definition for provider {provider_slug!r} in {fetchers_yml!r}"
