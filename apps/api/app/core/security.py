MAX_MESSAGE_CHARS = 8000
MAX_BODY_BYTES = 32 * 1024


def redact(value: str) -> str:
    if not value:
        return value
    if len(value) <= 8:
        return "********"
    return f"{value[:4]}...{value[-4:]}"
