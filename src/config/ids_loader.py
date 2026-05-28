import json
from pathlib import Path


def load_ids(env: str) -> dict:
    project_root = Path(__file__).resolve().parents[2]
    p = project_root / "data" / f"ids.{env}.json"
    if not p.exists():
        raise FileNotFoundError(f"IDs file not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))
