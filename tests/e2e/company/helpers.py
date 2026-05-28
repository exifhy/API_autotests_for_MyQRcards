import pytest
from http import HTTPStatus

from src.resources.api import companies_list, get_company_json, get_designsettings_json
from src.resources.helpers import find_company_in_list, is_background_removed, is_logo_removed
from src.support.waiter import wait_until
from src.utils.randoms import rand_email, rand_word


def require_ctx(ctx: dict, key: str, reason: str):
    value = ctx.get(key)
    if not value:
        pytest.skip(f"{reason} (missing ctx['{key}']). Upstream step failed or was skipped.")
    return value


def build_simple_company_payload() -> dict:
    suffix = rand_word("suf", 10).replace("suf_", "")
    return {
        "Name": f"AT_Company_{suffix}",
        "Phone": "+78129875643#1234335",
        "Fax": "+78129875643",
        "Email": rand_email(domain="tt.tt"),
        "SiteUrl": "https://www.test.tt",
        "FoundedYear": 2020,
        "Activity": "Test_api_company",
        "Customers": "Test_api_company",
    }


def wait_company_present_in_list(lk_api, company_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _present():
        response = companies_list(lk_api)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json()
        if not isinstance(items, list):
            return None
        return find_company_in_list(items, company_id=company_id)

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_company_get_json(lk_api, company_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _get_ok():
        data = get_company_json(lk_api, company_id)
        return data if isinstance(data, dict) else None

    return wait_until(_get_ok, timeout_s=timeout_s, step_s=step_s)


def wait_company_absent(lk_api, company_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _absent():
        response = lk_api.get(f"/companies/{int(company_id)}")
        return True if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND) else None

    return wait_until(_absent, timeout_s=timeout_s, step_s=step_s)


def wait_company_matches(
    lk_api,
    company_id: int,
    *,
    expected_name: str,
    expected_email: str,
    expect_logo_removed: bool = False,
    timeout_s: int = 60,
    step_s: int = 3,
):
    def _ok():
        data = get_company_json(lk_api, company_id)
        if data is None:
            return None

        name = data.get("name") or data.get("Name")
        email = data.get("email") or data.get("Email")
        if name != expected_name or email != expected_email:
            return None

        if expect_logo_removed:
            return True if is_logo_removed(data) else None
        return data

    return wait_until(_ok, timeout_s=timeout_s, step_s=step_s)


def wait_company_designsettings_match(
    lk_api,
    company_id: int,
    *,
    expected_color: str,
    expected_qr_color: str,
    expected_background_id: int | None = None,
    expect_background_removed: bool = False,
    timeout_s: int = 60,
    step_s: int = 3,
):
    def _ok():
        data = get_designsettings_json(lk_api, company_id)
        if data is None:
            return None

        color = data.get("color") or data.get("Color")
        qr_color = data.get("qrColor") or data.get("QRColor")
        if color != expected_color or qr_color != expected_qr_color:
            return None

        if expect_background_removed:
            return True if is_background_removed(data) else None

        background = data.get("backgroundAttachmentID") or data.get("BackgroundAttachmentID")
        try:
            background_int = int(background) if background is not None else None
        except Exception:
            background_int = None
        return data if background_int == int(expected_background_id) else None

    return wait_until(_ok, timeout_s=timeout_s, step_s=step_s)
