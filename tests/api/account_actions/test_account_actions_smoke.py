import os
import secrets
import uuid
from http import HTTPStatus

import allure
import pytest

from config.headers import Headers
from services.account_actions.account_actions_mobile_account_notification_send.api_account_actions_mobile_account_notification_send import (
    AccountActionsMobileAccountNotificationSendAPI,
)
from services.account_actions.account_actions_mobile_account_selfreg_verification.api_account_actions_mobile_account_selfreg_verification import (
    AccountActionsMobileAccountSelfRegVerificationAPI,
)
from services.account_actions.account_actions_mobile_account_verification.api_account_actions_mobile_account_verification import (
    AccountActionsMobileAccountVerificationAPI,
)
from services.account_actions.account_actions_subscription_invitation.api_account_actions_subscription_invitation import (
    AccountActionsSubscriptionInvitationAPI,
)
from services.account_actions.account_actions_web_account_verification.api_account_actions_web_account_verification import (
    AccountActionsWebAccountVerificationAPI,
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


def _account_actions_url() -> str:
    from config.config import HOST
    return HOST.rstrip("/") + "/accountActions"


@allure.epic("API")
@allure.feature("AccountActions")
@pytest.mark.api
@pytest.mark.smoke
class TestAccountActionsSmoke:
    @allure.title("012 MobileAccountVerification smoke")
    def test_mobile_account_verification_accepts_random_email(self):
        password, app_id = _require_account_actions_password()
        random_email = _random_email()
        suffix = _random_suffix()

        response, model, payload = AccountActionsMobileAccountVerificationAPI().create_mobile_account_verification(
            app_id=app_id,
            push_token=f"smoke_push_{suffix}",
            client_name=f"smoke_client_{suffix}",
            basic_login=random_email,
            basic_password=password,
        )

        assert response.status_code == HTTPStatus.ACCEPTED, f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        assert getattr(model, "actionJwt", None), "012 did not return actionJwt"
        assert getattr(model, "actionToken", None), "012 did not return actionToken"
        assert payload["pushToken"].endswith(suffix)

    @allure.title("012 -> 020 smoke with actionJwt")
    def test_mobile_account_verification_then_get_account_actions(self):
        password, app_id = _require_account_actions_password()
        random_email = _random_email()
        suffix = _random_suffix()

        response, model, _ = AccountActionsMobileAccountVerificationAPI().create_mobile_account_verification(
            app_id=app_id,
            push_token=f"smoke_push_{suffix}",
            client_name=f"smoke_client_{suffix}",
            basic_login=random_email,
            basic_password=password,
        )

        assert response.status_code == HTTPStatus.ACCEPTED, f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        action_jwt = getattr(model, "actionJwt", None)
        assert action_jwt, "012 did not return actionJwt"

        response_020 = _helper._call(
            "GET",
            url=_account_actions_url(),
            headers=Headers.auth_header(bearer_token=str(action_jwt), app_id=app_id),
        )

        assert response_020.status_code == HTTPStatus.OK, f"Expected HTTPStatus.OK, got {response_020.status_code}: {response_020.text}"
        data = response_020.json() if response_020.text else {}
        assert isinstance(data, dict), f"Expected dict response, got {type(data)} / {data}"
        assert data.get("validTill"), f"020 did not return validTill: {data}"
        assert data.get("repeatAfter"), f"020 did not return repeatAfter: {data}"

    @allure.title("011 WebAccountVerification smoke — random push_token → not 5xx")
    def test_web_account_verification_smoke(self):
        suffix = _random_suffix()
        response, _, _ = AccountActionsWebAccountVerificationAPI().create_web_account_verification(
            push_token=f"smoke_push_{suffix}",
            client_name=f"smoke_client_{suffix}",
        )
        assert response.status_code < 500, f"Server error on 011: {response.status_code}: {response.text}"

    @allure.title("013 SubscriptionInvitation smoke — random push_token → not 5xx")
    def test_subscription_invitation_smoke(self):
        suffix = _random_suffix()
        response, _, _ = AccountActionsSubscriptionInvitationAPI().create_subscription_invitation_action(
            push_token=f"smoke_push_{suffix}",
            client_name=f"smoke_client_{suffix}",
        )
        assert response.status_code < 500, f"Server error on 013: {response.status_code}: {response.text}"

    @allure.title("014 MobileAccountSelfRegVerification smoke — random push_token + guid → not 5xx")
    def test_mobile_account_selfreg_verification_smoke(self):
        suffix = _random_suffix()
        response, _, _ = AccountActionsMobileAccountSelfRegVerificationAPI().create_mobile_account_selfreg_verification(
            push_token=f"smoke_push_{suffix}",
            guid=str(uuid.uuid4()),
        )
        assert response.status_code < 500, f"Server error on 014: {response.status_code}: {response.text}"

    @allure.title("015 MobileAccountNotificationSend smoke — random push_token + guid → not 5xx")
    def test_mobile_account_notification_send_smoke(self):
        suffix = _random_suffix()
        response, _, _ = AccountActionsMobileAccountNotificationSendAPI().create_mobile_account_notification_send(
            push_token=f"smoke_push_{suffix}",
            guid=str(uuid.uuid4()),
        )
        assert response.status_code < 500, f"Server error on 015: {response.status_code}: {response.text}"

    @allure.title("012.2 MobileAccountVerification/silent smoke — 202 + actionJwt, без письма")
    def test_mobile_account_verification_silent_smoke(self):
        password, app_id = _require_account_actions_password()
        suffix = _random_suffix()

        response, model, _ = AccountActionsMobileAccountVerificationAPI().create_mobile_account_verification_silent(
            app_id=app_id,
            push_token=f"smoke_push_{suffix}",
            client_name=f"smoke_client_{suffix}",
            basic_login=_random_email(),
            basic_password=password,
        )

        assert response.status_code == HTTPStatus.ACCEPTED, f"Expected 202, got {response.status_code}: {response.text}"
        assert getattr(model, "actionJwt", None), "012.2 silent did not return actionJwt"
        assert getattr(model, "actionToken", None), "012.2 silent did not return actionToken"

    @allure.title("011.2 WebAccountVerification/silent smoke — not 5xx, без письма")
    def test_web_account_verification_silent_smoke(self):
        suffix = _random_suffix()
        response, _, _ = AccountActionsWebAccountVerificationAPI().create_web_account_verification_silent(
            push_token=f"smoke_push_{suffix}",
            client_name=f"smoke_client_{suffix}",
        )
        assert response.status_code < 500, f"Server error on 011.2 silent: {response.status_code}: {response.text}"
