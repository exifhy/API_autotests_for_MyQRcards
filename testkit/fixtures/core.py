import os
from pathlib import Path

import pytest

from src.api.lk_client import LkApiClient
from src.config.env_loader import getenv_required
from src.config.ids_loader import load_ids
from testkit.generated_assets import create_generated_assets


def _opt_int(ids: dict, key: str):
    val = ids.get(key)
    return int(val) if val not in (None, "", 0, "0") else None


@pytest.fixture(scope="session")
def cfg(env) -> dict:
    ids = load_ids(env)
    return {
        "env": env,
        "host": str(ids["host"]).rstrip("/"),
        "x_application_id": str(ids.get("x_application_id", "")),
        "lk_account_id": _opt_int(ids, "lk_account_id"),
        "mobile_account_id": _opt_int(ids, "mobile_account_id"),
        "company_id_source": _opt_int(ids, "company_id_source"),
        "company_id_target": _opt_int(ids, "company_id_target"),
        "company_id_create": _opt_int(ids, "company_id_create"),
        "subscription_id": _opt_int(ids, "subscription_id"),
        "lk_email": (ids.get("lk_email") or "").strip(),
        "lk_contact_id": _opt_int(ids, "lk_contact_id"),
        "lk_jwt": getenv_required("LK_JWT"),
        "mobile_jwt": os.getenv("MOBILE_JWT") or os.getenv("ACCESS_JWT_MOBILE") or "",
    }


@pytest.fixture(scope="session")
def lk_api(cfg) -> LkApiClient:
    return LkApiClient(
        host=cfg["host"],
        token=cfg["lk_jwt"],
        x_application_id=cfg.get("x_application_id") or None,
    )


@pytest.fixture(scope="session")
def generated_assets(tmp_path_factory) -> dict:
    root = Path(tmp_path_factory.mktemp("generated_assets"))
    return create_generated_assets(root)
