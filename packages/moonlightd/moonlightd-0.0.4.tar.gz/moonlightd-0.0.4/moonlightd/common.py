def fmt_italic(s: str) -> str:
    if not s:
        return ""
    return f"<i>{s}</i>"


def fmt_bold(s: str) -> str:
    if not s:
        return ""
    return f"<b>{s}</b>"


def fmt_code(s: str) -> str:
    if not s:
        return ""
    return f"<code>{s}</code>"


def fmt_pre_block(s: str) -> str:
    return f"<pre>{s}</pre>"
