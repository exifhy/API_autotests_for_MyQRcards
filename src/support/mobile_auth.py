import os

from loguru import logger

from config.headers import Headers
from src.support.helper import Helper
from src.support.token_utils import get_manager_jwt, get_manager_password


def get_fresh_access_jwt(
    *, login: str | None = None, push_token: str = "autotest_refresh", client_name: str = "autotest_refresh"
) -> str | None:
    """Mints a fresh session JWT for the given account email, without email/manual steps:
    012.2 MobileAccountVerification/silent -> 912 Manager/confirmlogin -> 020 GET /accountActions -> 040 POST /accounts/authorize.
    Returns None (caller should fall back to a static token) if any prerequisite/step fails.
    `login` defaults to ACCOUNT_ACTIONS_BASIC_LOGIN (the mobile-app test account) if not given.
    """
    login = login or os.getenv("ACCOUNT_ACTIONS_BASIC_LOGIN")
    password = os.getenv("ACCOUNT_ACTIONS_BASIC_PASSWORD")
    manager_jwt = get_manager_jwt()
    manager_password = get_manager_password()
    app_id = os.getenv("APP_ID") or "3"

    if not all([login, password, manager_jwt, manager_password]):
        logger.debug("[mobile_auth] Skipped: ACCOUNT_ACTIONS_BASIC_LOGIN/PASSWORD or manager creds not configured")
        return None

    try:
        from config.config import HOST
        from services.account_actions.account_actions_get.api_account_actions_get import AccountActionsGetAPI
        from services.account_actions.account_actions_mobile_account_verification.api_account_actions_mobile_account_verification import (
            AccountActionsMobileAccountVerificationAPI,
        )

        helper = Helper()

        _, action_model, _ = AccountActionsMobileAccountVerificationAPI().create_mobile_account_verification_silent(
            app_id=app_id,
            push_token=push_token,
            client_name=client_name,
            basic_login=login,
            basic_password=password,
        )
        action_jwt = getattr(action_model, "actionJwt", None)
        if not action_jwt:
            logger.debug("[mobile_auth] Step 012.2 did not return actionJwt")
            return None

        confirm_response = helper._call(
            "POST",
            url=f"{HOST}/Manager/confirmlogin",
            headers=Headers.auth_header(bearer_token=manager_jwt, app_id=app_id),
            json={"managerPassword": manager_password, "email": login},
        )
        if confirm_response.status_code != 204:
            logger.debug(f"[mobile_auth] Step 912 confirmlogin failed: {confirm_response.status_code}")
            return None

        _, get_model = AccountActionsGetAPI().get_account_actions_by_token(bearer_token=str(action_jwt), app_id=app_id)
        account_client_jwt = next(
            (item.get("accountClientJwt") for item in get_model.raw if item.get("accountClientJwt")), None
        )
        if not account_client_jwt:
            logger.debug(f"[mobile_auth] Step 020 did not return accountClientJwt: {get_model.raw}")
            return None

        authorize_response = helper._call(
            "POST",
            url=f"{HOST}/accounts/authorize",
            headers=Headers.auth_header(bearer_token=account_client_jwt),
        )
        if authorize_response.status_code != 200:
            logger.debug(f"[mobile_auth] Step 040 authorize failed: {authorize_response.status_code}")
            return None

        access_jwt = authorize_response.json().get("accessJwt")
        if access_jwt:
            logger.debug("[mobile_auth] Fresh mobile access JWT minted successfully")
        return access_jwt
    except Exception as exc:
        logger.debug(f"[mobile_auth] Refresh flow raised {exc!r}")
        return None
