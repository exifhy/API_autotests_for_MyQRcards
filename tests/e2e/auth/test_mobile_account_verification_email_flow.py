import os
import time
from datetime import datetime, timezone
from http import HTTPStatus

import allure
import pytest

from services.account_actions.account_actions_get.api_account_actions_get import AccountActionsGetAPI
from requests import Response
from services.account_actions.account_actions_get.models.account_actions_get_model import AccountActionsGetModel
from src.support.helper import Helper
from services.account_actions.account_actions_mobile_account_verification.api_account_actions_mobile_account_verification import (
    AccountActionsMobileAccountVerificationAPI,
)
from services.accounts.accounts_authorize.api_accounts_authorize import AccountsAuthorizeAPI
from src.support.test_mailbox import (
    choose_confirm_url,
    extract_urls_from_message,
    find_fresh_verification_email,
    get_message_by_uid,
)
from src.support.waiter import wait_until


def _require_basic_auth_credentials() -> tuple[str, str, str]:
    login = os.getenv("ACCOUNT_ACTIONS_BASIC_LOGIN")
    password = os.getenv("ACCOUNT_ACTIONS_BASIC_PASSWORD")
    app_id = os.getenv("APP_ID") or "3"
    if not login or not password:
        pytest.skip(
            "AccountActions auth flow is not configured: "
            "set ACCOUNT_ACTIONS_BASIC_LOGIN and ACCOUNT_ACTIONS_BASIC_PASSWORD"
        )
    return login, password, app_id


_helper = Helper()


def _handle_409_conflict(response: Response) -> None:
    body = response.text or ""
    repeat_after = None
    try:
        repeat_after = _find_in_json(response.json(), {"repeatAfter", "RepeatAfter"})
    except Exception:
        pass

    if "AlreadyDone" in body or "Выполнено ранее" in body:
        msg = (
            f"Account is not ready for repeated verification yet. repeatAfter={repeat_after}"
            if repeat_after
            else "Account is already verified. Use a fresh unverified mailbox."
        )
        pytest.skip(msg)
    pytest.fail(f"POST /accountActions/MobileAccountVerification returned 409: {body}")


def _find_in_json(data, keys: set[str]) -> str | None:
    if isinstance(data, dict):
        for k, v in data.items():
            if k in keys:
                return str(v) if v is not None else None
            found = _find_in_json(v, keys)
            if found is not None:
                return found
    elif isinstance(data, list):
        for item in data:
            found = _find_in_json(item, keys)
            if found is not None:
                return found
    return None


def _extract_action_jwt(model) -> str | None:
    for attr in ("actionJwt", "actionJWT"):
        val = getattr(model, attr, None)
        if val:
            return str(val)
    extras = getattr(model, "model_extra", None) or {}
    return _find_in_json(extras, {"actionJwt", "actionJWT", "actionToken"})


def _poll_for_access_jwt(
    api: AccountActionsGetAPI, action_jwt: str, app_id: str
) -> tuple[Response, AccountActionsGetModel] | None:
    response, model = api.get_account_actions_by_token(action_jwt, app_id=app_id)
    return (response, model) if model.access_jwt else None


@allure.epic("LK")
@allure.feature("Auth")
@pytest.mark.e2e
@pytest.mark.external
@allure.description(
    """
    012  POST /accountActions/MobileAccountVerification  → actionJwt
    020  GET  /accountActions (before confirmation)
         email confirmation via link from mailbox
    020  GET  /accountActions — poll until accessJWT
    040.1 POST /accounts/authorize (with accessJWT)
    """
)
class TestMobileAccountVerificationEmailFlow:

    @pytest.mark.skip(reason="Requires a fresh unverified mailbox account — configure a dedicated test account in env")
    @allure.title("Mobile account verification: 012 → email → confirm → 020 → 040.1")
    def test_mobile_account_verification_email_arrives(self):
        login, password, app_id = _require_basic_auth_credentials()
        started_at = datetime.now(timezone.utc)
        now = int(time.time())

        with allure.step("012  POST /accountActions/MobileAccountVerification"):
            response, model, _ = AccountActionsMobileAccountVerificationAPI().create_mobile_account_verification(
                app_id=app_id,
                push_token=f"autotests_push_{now}",
                client_name=f"autotests_client_{now}",
                basic_login=login,
                basic_password=password,
            )
            if response.status_code == HTTPStatus.CONFLICT:
                _handle_409_conflict(response)

        action_jwt = _extract_action_jwt(model)
        assert action_jwt, "012 did not return actionJwt"

        actions_api = AccountActionsGetAPI()

        with allure.step("020  GET /accountActions (before confirmation)"):
            response_before, _ = actions_api.get_account_actions_by_token(action_jwt, app_id=app_id)
            allure.attach(response_before.text or "<empty>", "state_before_confirm", allure.attachment_type.JSON)

        with allure.step("Wait for verification email (timeout 90s)"):
            message_item = wait_until(
                lambda: find_fresh_verification_email(started_at=started_at),
                timeout_s=90,
                step_s=5,
            )
            assert message_item is not None, "Verification email not received within 90 seconds"

        with allure.step("Extract confirm URL from email and follow it"):
            message = get_message_by_uid(message_item.uid)
            allure.attach(message.subject or "<empty>", "mail_subject", allure.attachment_type.TEXT)
            allure.attach(message.from_ or "<empty>", "mail_from", allure.attachment_type.TEXT)
            allure.attach(message.text_body or "<empty>", "mail_text_body", allure.attachment_type.TEXT)
            allure.attach(message.html_body or "<empty>", "mail_html_body", allure.attachment_type.HTML)

            urls = extract_urls_from_message(message)
            assert urls, "No URLs found in verification email"
            confirm_url = choose_confirm_url(urls)
            assert confirm_url, "No confirmation URL found in verification email"
            allure.attach(confirm_url, "confirm_url", allure.attachment_type.TEXT)

            confirm_response = _helper._call("GET", url=confirm_url, allow_redirects=True)
            assert confirm_response.status_code in (
                HTTPStatus.OK,
                HTTPStatus.MOVED_PERMANENTLY,
                HTTPStatus.FOUND,
                HTTPStatus.SEE_OTHER,
                HTTPStatus.TEMPORARY_REDIRECT,
                HTTPStatus.PERMANENT_REDIRECT,
            ), f"Confirm URL returned unexpected status {confirm_response.status_code}"

        with allure.step("020  GET /accountActions — poll until accessJWT (timeout 60s)"):
            result = wait_until(
                lambda: _poll_for_access_jwt(actions_api, action_jwt, app_id),
                timeout_s=60,
                step_s=5,
            )
            assert result is not None, "GET /accountActions did not return accessJWT within 60 seconds after confirmation"
            response_after, model_after = result
            allure.attach(response_after.text or "<empty>", "state_after_confirm", allure.attachment_type.JSON)

        access_jwt = model_after.access_jwt
        assert access_jwt, "GET /accountActions after confirmation did not return accessJWT"
        allure.attach(access_jwt, "access_jwt", allure.attachment_type.TEXT)

        with allure.step("040.1  POST /accounts/authorize (with accessJWT)"):
            _, authorize_model = AccountsAuthorizeAPI().authorize_account_with_token(
                bearer_token=access_jwt,
                app_id=app_id,
            )
            assert authorize_model.accountID, "POST /accounts/authorize did not return accountID"
            allure.attach(str(authorize_model.accountID), "account_id", allure.attachment_type.TEXT)
            allure.attach(authorize_model.email or "<empty>", "account_email", allure.attachment_type.TEXT)
