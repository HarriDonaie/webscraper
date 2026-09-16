from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    actual_url = parsed.netloc
    if parsed.path:
        actual_url += parsed.path
    if parsed.query:
        actual_url += "?" + parsed.query
    if parsed.fragment:
        actual_url += "#" + parsed.fragment
    return actual_url