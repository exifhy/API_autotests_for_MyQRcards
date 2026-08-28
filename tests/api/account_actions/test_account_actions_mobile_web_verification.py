import os
import secrets
from http import HTTPStatus

import allure
import pytest

from config.config import HOST
from config.headers import Headers
from services.account_actions.account_actions_get.api_account_actions_get import AccountActionsGetAPI
from services.account_actions.account_actions_mobile_web_account_verification.api_account_actions_mobile_web_account_verification import (
    AccountActionsMobileWebAccountVerificationAPI,
)
from src.support.helper import Helper

_helper = Helper()


def _require_account_actions_password() -> tuple[str, str]:
    password = os.getenv("ACCOUNT_ACTIONS_BASIC_PASSWORD")
    app_id = os.getenv("APP_ID") or "3"
    if not password:
        pytest.skip("ACCOUNT_ACTIONS_BASIC_PASSWORD is not configured")
    return password, app_id


def _random_email() -> str:
    return f"autotest_{secrets.token_hex(6)}@gmail.com"


def _random_suffix() -> str:
    return secrets.token_hex(4)


@allure.epic("API")
@allure.feature("AccountActions")
@pytest.mark.api
@allure.description(
    """
    /accountActions/MobileWebAccountVerification (REQUIREMENT 32516) — авторизация в веб-версию МП,
    аналог MobileAccountVerification без инициализации онбординг-пушей.
    """
)
class TestAccountActionsMobileWebVerification:
    @allure.title("MobileWebAccountVerification smoke — 202 + actionJwt/actionToken")
    @pytest.mark.smoke
    def test_mobile_web_account_verification_accepts_random_email(self):
        password, app_id = _require_account_actions_password()
        suffix = _random_suffix()

        response, model, payload = AccountActionsMobileWebAccountVerificationAPI().create_mobile_web_account_verification(
            app_id=app_id,
            client_name=f"smoke_client_{suffix}",
            basic_login=_random_email(),
            basic_password=password,
        )

        assert response.status_code == HTTPStatus.ACCEPTED, f"Expected 202, got {response.status_code}: {response.text}"
        assert getattr(model, "actionJwt", None), "MobileWebAccountVerification did not return actionJwt"
        assert getattr(model, "actionToken", None), "MobileWebAccountVerification did not return actionToken"
        assert payload["clientName"] == f"smoke_client_{suffix}"

    @allure.title("MobileWebAccountVerification/silent smoke — 202 + actionJwt/actionToken, без письма")
    @pytest.mark.smoke
    def test_mobile_web_account_verification_silent_smoke(self):
        password, app_id = _require_account_actions_password()
        suffix = _random_suffix()

        response, model, _ = AccountActionsMobileWebAccountVerificationAPI().create_mobile_web_account_verification_silent(
            app_id=app_id,
            client_name=f"smoke_client_{suffix}",
            basic_login=_random_email(),
            basic_password=password,
        )

        assert response.status_code == HTTPStatus.ACCEPTED, f"Expected 202, got {response.status_code}: {response.text}"
        assert getattr(model, "actionJwt", None), "silent variant did not return actionJwt"
        assert getattr(model, "actionToken", None), "silent variant did not return actionToken"

    @allure.title("MobileWebAccountVerification -> 020 GET /accountActions with actionJwt")
    def test_mobile_web_account_verification_then_get_account_actions(self):
        password, app_id = _require_account_actions_password()
        suffix = _random_suffix()

        response, model, _ = AccountActionsMobileWebAccountVerificationAPI().create_mobile_web_account_verification(
            app_id=app_id,
            client_name=f"smoke_client_{suffix}",
            basic_login=_random_email(),
            basic_password=password,
        )
        assert response.status_code == HTTPStatus.ACCEPTED

        action_jwt = getattr(model, "actionJwt", None)
        assert action_jwt, "did not return actionJwt"

        get_response, get_model = AccountActionsGetAPI().get_account_actions_by_token(
            bearer_token=str(action_jwt), app_id=app_id
        )
        assert get_response.status_code == HTTPStatus.OK
        assert get_model.raw, f"Expected non-empty accountActions data: {get_model.raw}"
        item = get_model.raw[0]
        assert item.get("validTill"), f"020 did not return validTill: {item}"
        assert item.get("repeatAfter"), f"020 did not return repeatAfter: {item}"

    # NOTE: a "full login chain via Manager/confirmlogin" test was attempted here and removed.
    # ADM.AccountLoginConfirm (the SP behind POST /Manager/confirmlogin) explicitly filters
    # `ActionID in (1, 3)` — MobileAccountVerification / WebAccountVerification only. ActionID 13
    # (MobileWebAccountVerification, this requirement) is NOT included, so the Manager-assisted
    # confirm bypass cannot confirm this action type — see REQUIREMENT 32516 checklist finding.
    # A true end-to-end confirm for this action would need the real email-link flow
    # (src/support/test_mailbox.py), not the Manager bypass used elsewhere in this project today.

    @allure.title("MobileWebAccountVerification with an arbitrary Basic password for a brand-new email -> still 202")
    def test_mobile_web_account_verification_new_email_any_password_accepted(self):
        # For an email with no existing account yet there is no ClientID/password to validate against —
        # any Basic password is accepted and becomes the new device identity (same as MobileAccountVerification).
        _, app_id = _require_account_actions_password()
        suffix = _random_suffix()

        response, model, _ = AccountActionsMobileWebAccountVerificationAPI().create_mobile_web_account_verification(
            app_id=app_id,
            client_name=f"neg_client_{suffix}",
            basic_login=_random_email(),
            basic_password="any-arbitrary-client-id-value",
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected 202, got {response.status_code}: {response.text}"
        )
        assert getattr(model, "actionJwt", None)

    @allure.title("MobileWebAccountVerification without Authorization header at all -> 409 ParameterNull")
    @pytest.mark.ng
    def test_mobile_web_account_verification_without_auth_header_409(self):
        _, app_id = _require_account_actions_password()
        suffix = _random_suffix()

        response = _helper._call(
            "POST",
            url=f"{HOST}/accountActions/MobileWebAccountVerification",
            headers=Headers.without_authorization_field_header(app_id=app_id),
            json={"pushToken": "", "clientName": f"neg_client_{suffix}", "IsAcceptAdvertising": False},
        )
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected 409 (ParameterNull — missing Authorization header), got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data[0]["code"] == "ParameterNull", f"Expected code=ParameterNull, got: {data}"
