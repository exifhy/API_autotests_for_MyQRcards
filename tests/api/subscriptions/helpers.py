from http import HTTPStatus

from config.headers import Headers
from services.accounts.accounts_list.endpoints import Endpoints
from src.support.helper import Helper
from src.support.waiter import wait_until
from src.support.token_utils import get_token

_helper = Helper()


def _get_accounts_raw(*, invite_id: int):
    return _helper._call(
        "GET",
        url=Endpoints.get_accounts_list_endpoint,
        headers=Headers.auth_header(bearer_token=get_token(), Range="items=0-50"),
        params={"accountID": str(int(invite_id))},
    )


def wait_subscription_invitation_account_present(
    *,
    invite_id: int,
    expected_email: str,
    timeout_s: int = 60,
    step_s: int = 3,
):
    def _present():
        response = _get_accounts_raw(invite_id=int(invite_id))
        if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
            return None
        items = response.json() if response.text else []
        if not isinstance(items, list):
            return None
        for item in items:
            if not isinstance(item, dict):
                continue
            if int(item.get("id", 0)) != int(invite_id):
                continue
            email = str(item.get("email") or "").strip().lower()
            if email == str(expected_email).strip().lower():
                return item
        return None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_subscription_invitation_account_absent(
    *,
    invite_id: int,
    timeout_s: int = 60,
    step_s: int = 3,
):
    def _absent():
        response = _get_accounts_raw(invite_id=int(invite_id))
        if response.status_code == HTTPStatus.NO_CONTENT:
            return True
        if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
            return None
        items = response.json() if response.text else []
        if not isinstance(items, list):
            return None
        return True if not any(int(item.get("id", 0)) == int(invite_id) for item in items if isinstance(item, dict)) else None

    return wait_until(_absent, timeout_s=timeout_s, step_s=step_s)
