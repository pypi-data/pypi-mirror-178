import re

URL_RE = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"  # noqa
URL_RE_SINGLE = re.compile(f"^{URL_RE}$")
URL_RE_MULTI = re.compile(URL_RE)


def is_url(value: str) -> bool:
    return bool(URL_RE_SINGLE.match(value))
