import base64
import json


def decode_jwt_payload(jwt_str: str) -> dict:
    """Decodes (does not verify signature) the payload segment of a JWT — enough
    to inspect what data an API embedded in it (e.g. Google Wallet save JWTs)."""
    payload_b64 = jwt_str.split(".")[1]
    padding = "=" * (-len(payload_b64) % 4)
    decoded = base64.urlsafe_b64decode(payload_b64 + padding)
    return json.loads(decoded)
