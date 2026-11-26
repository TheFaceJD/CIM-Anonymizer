
import hashlib
import hmac
import secrets
from pathlib import Path


KEY_FILE = Path(__file__).resolve().parent / "anonymization.key"


def load_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()

    key = secrets.token_bytes(32)
    KEY_FILE.write_bytes(key)
    return key


def make_pseudonym(value, category):
    if value is None or value == "":
        return value

    key = load_key()

    message = f"{category}:{value}".encode("utf-8")

    digest = hmac.new(
        key,
        message,
        hashlib.sha256
    ).hexdigest()[:20]

    return f"{category}_{digest}"
