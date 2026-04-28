from datetime import UTC, datetime, timedelta
import os
import sys
from pathlib import Path

import pytest
import requests
from loguru import logger

from config.config import get_host
from config.headers import Headers
from src.config.env_loader import load_env
from src.config.ids_loader import load_ids
from src.support.env import get_api_user_token

pytest_plugins = [
    "testkit.fixtures.core",
    "testkit.fixtures.employee",
    "testkit.fixtures.mobile",
]

TOKEN_EXPIRATION_TIME = datetime.min.replace(tzinfo=UTC)
BEARER_TOKEN = None
APP_ID = os.getenv("APP_ID")


def _resolve_host() -> str:
    return get_host()


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=("dev", "prod"),
        help="Environment to run tests against",
    )
    parser.addoption("--runs", action="store", default=1, help="Number of scenario runs")


def pytest_configure(config):
    env_name = config.getoption("--env")
    load_env(env_name)
    _hydrate_env_from_ids(env_name)
    logger.debug(f"[pytest_configure] Loaded .env.{env_name}")
    _write_allure_environment(config, env_name)
    _write_allure_categories(config)


def _hydrate_env_from_ids(env_name: str) -> None:
    ids = load_ids(env_name)
    host = str(ids.get("host") or os.getenv("HOST") or "").rstrip("/")
    if host:
        os.environ["HOST"] = host
        os.environ[f"URL_{env_name.upper()}_API"] = host

    app_id = ids.get("x_application_id")
    if app_id not in (None, "") and not os.getenv("APP_ID"):
        os.environ["APP_ID"] = str(app_id)


def _write_allure_environment(config, env_name: str) -> None:
    allure_dir = config.getoption("--alluredir")
    if not allure_dir:
        return

    host = _resolve_host()
    ids = load_ids(env_name)
    app_id = str(ids.get("x_application_id") or os.getenv("APP_ID") or "")

    run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    lines = [
        "PROJECT=autotests_MyQRcards",
        "SERVICE=lk-api",
        f"ENVIRONMENT={env_name}",
        f"HOST={host}",
        f"APP_ID={app_id}",
        f"DATE={run_date}",
        f"PYTHON={python_version}",
    ]

    output_dir = Path(allure_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "environment.properties").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def _write_allure_categories(config) -> None:
    allure_dir = config.getoption("--alluredir")
    if not allure_dir:
        return

    source_path = Path("config") / "allure_categories.json"
    if not source_path.exists():
        logger.warning("Allure categories template not found: {}", source_path)
        return

    output_dir = Path(allure_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "categories.json").write_text(
        source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def _get_api_user_access_token():
    global TOKEN_EXPIRATION_TIME, BEARER_TOKEN
    now = datetime.now(UTC)
    if BEARER_TOKEN and now < TOKEN_EXPIRATION_TIME:
        return BEARER_TOKEN

    service_token = get_api_user_token()
    if not service_token:
        return None

    response = requests.post(
        url=f"{_resolve_host()}/AUTHZ/AccessTokens/",
        headers=Headers.basic_content_type,
        json={"serviceToken": service_token},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    BEARER_TOKEN = data["access_token"]
    TOKEN_EXPIRATION_TIME = now + timedelta(minutes=25)
    return BEARER_TOKEN


def pytest_sessionstart() -> None:
    token = _get_api_user_access_token()
    if token:
        os.environ["API_TOKEN"] = token
        logger.debug("[session] API token acquired and stored in API_TOKEN")
    else:
        logger.debug("[session] API_USER_TOKEN not set — API_TOKEN skipped")


def pytest_runtest_setup() -> None:
    token = _get_api_user_access_token()
    if token:
        os.environ["API_TOKEN"] = token


@pytest.fixture(scope="session")
def env(request) -> str:
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def leadgen_field_template_id():
    from services.leadgen.leadgen_form_fields.api_leadgen_form_fields import LeadGenFormFieldsAPI

    last_error = None
    for _ in range(2):
        try:
            _, field_templates = LeadGenFormFieldsAPI().get_leadgen_form_fields(offset=0, fetch=20)
            assert field_templates.items, "LeadGen form fields list is empty"
            field_template_id = next((item.id for item in field_templates.items if item.id is not None), None)
            assert field_template_id is not None, "No leadGen fieldTemplateID found"
            return int(field_template_id)
        except requests.RequestException as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    raise AssertionError("Failed to resolve leadGen fieldTemplateID")


@pytest.fixture(scope="session")
def api_token():
    token = _get_api_user_access_token()
    if token:
        logger.debug("API token acquired for test session")
    else:
        logger.debug("API token not acquired (API_USER_TOKEN is missing)")
    return token
