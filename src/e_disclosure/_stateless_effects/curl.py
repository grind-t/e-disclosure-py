import subprocess


def curl(*args: str, stdin: bytes | None = None) -> bytes:
    """Тело ответа ``curl -fsSL``: urllib зависает на IPv6."""
    return subprocess.run(
        ["curl", "-fsSL", *args], input=stdin, capture_output=True, check=True
    ).stdout
