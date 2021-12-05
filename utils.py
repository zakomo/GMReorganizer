from html import unescape

def sanitize_name(filename: str) -> str:
    return unescape(filename).replace("/", "-").replace("\\", "-").strip()
