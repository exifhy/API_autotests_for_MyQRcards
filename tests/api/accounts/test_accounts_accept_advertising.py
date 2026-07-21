import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_accept_advertising.api_accounts_accept_advertising import (
    AccountsAcceptAdvertisingAPI,
)
from services.accounts.accounts_get.api_accounts_get import AccountsGetAPI


def _get_flag(account_id: int) -> bool | None:
    return AccountsGetAPI().get_account(account_id).isAcceptAdvertising


@pytest.fixture
def accept_advertising_guard(cfg):
    """Читает исходное значение isAcceptAdvertising и восстанавливает его после теста.

    Ручка мутирует общий тестовый аккаунт (LK_JWT), поэтому оставлять флаг
    в изменённом состоянии нельзя.
    """
    account_id = cfg.get("lk_account_id")
    assert account_id, "cfg['lk_account_id'] is empty"
    original = _get_flag(int(account_id))

    yield int(account_id)

    try:
        AccountsAcceptAdvertisingAPI().update_accept_advertising(bool(original))
    except Exception:
        pass


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    PUT /accounts/this/acceptAdvertising (REQUIREMENT 26329)
    Согласие на рекламные рассылки. Флаг читается через GET /accounts/{id}.
    """
)
class TestAccountsAcceptAdvertising:
    @allure.title("PUT acceptAdvertising true -> 202, GET reflects true")
    @pytest.mark.smoke
    def test_accept_advertising_set_true(self, accept_advertising_guard):
        account_id = accept_advertising_guard

        response, _ = AccountsAcceptAdvertisingAPI().update_accept_advertising(True)
        assert response.status_code == HTTPStatus.ACCEPTED

        assert _get_flag(account_id) is True

    @allure.title("PUT acceptAdvertising false -> 202, GET reflects false")
    @pytest.mark.smoke
    def test_accept_advertising_set_false(self, accept_advertising_guard):
        account_id = accept_advertising_guard

        set_true, _ = AccountsAcceptAdvertisingAPI().update_accept_advertising(True)
        assert set_true.status_code == HTTPStatus.ACCEPTED

        response, _ = AccountsAcceptAdvertisingAPI().update_accept_advertising(False)
        assert response.status_code == HTTPStatus.ACCEPTED

        assert _get_flag(account_id) is not True

    @allure.title("PUT acceptAdvertising with empty body -> 202, flag falls back to false (binder default)")
    def test_accept_advertising_empty_body_defaults_to_false(self, accept_advertising_guard):
        account_id = accept_advertising_guard

        set_true, _ = AccountsAcceptAdvertisingAPI().update_accept_advertising(True)
        assert set_true.status_code == HTTPStatus.ACCEPTED

        response = AccountsAcceptAdvertisingAPI().update_accept_advertising_raw({})
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )

        assert _get_flag(account_id) is not True

    @allure.title("PUT acceptAdvertising with non-boolean value -> 400")
    @pytest.mark.ng
    def test_accept_advertising_invalid_type_400(self):
        response = AccountsAcceptAdvertisingAPI().update_accept_advertising_raw(
            {"isAcceptAdvertising": "yes"}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Expected HTTPStatus.BAD_REQUEST, got {response.status_code}: {response.text}"
        )

    @allure.title("PUT acceptAdvertising without auth -> 401")
    @pytest.mark.ng
    def test_accept_advertising_401_without_auth(self):
        response = AccountsAcceptAdvertisingAPI().update_accept_advertising_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
