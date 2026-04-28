import os
from pathlib import Path

from dotenv import load_dotenv


def load_env(env: str) -> None:
    project_root = Path(__file__).resolve().parents[2]
    env_file = project_root / f".env.{env}"
    if not env_file.exists():
        raise FileNotFoundError(f"Env file not found: {env_file}")
    load_dotenv(dotenv_path=env_file, override=True)


def getenv_required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Environment variable '{name}' is not set")
    return val
