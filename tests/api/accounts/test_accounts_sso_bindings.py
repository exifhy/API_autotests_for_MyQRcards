import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_sso_bindings.api_sso_bindings import AccountsSsoBindingsAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    GET /Accounts/sso
    301 — список SSO-провайдеров, привязанных к текущему аккаунту.
    Требует Bearer авторизации.
    Возвращает 200 со списком привязок или 204 если привязок нет.
    """
)
class TestAccountsSsoBindings:
    @allure.title("GET /Accounts/sso — returns 200 or 204")
    @pytest.mark.smoke
    def test_sso_bindings_200_or_204(self):
        response, bindings = AccountsSsoBindingsAPI().get_sso_bindings()

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Unexpected status: {response.status_code}: {response.text}"
        )

    # test_sso_bindings_structure — закомментирован: тест-аккаунт не имеет привязанных SSO,
    # всегда приходит 204 → pytest.skip → замусоривает Allure.
    # Раскомментировать когда на dev-аккаунте будет привязан VK ID или Яндекс ID.
    #
    # @allure.title("GET /Accounts/sso — each binding has providerType, providerCode and isVerified")
    # def test_sso_bindings_structure(self):
    #     response, bindings = AccountsSsoBindingsAPI().get_sso_bindings()
    #     if response.status_code == HTTPStatus.NO_CONTENT:
    #         pytest.skip("No SSO bindings on test account (204)")
    #     for b in bindings:
    #         assert b.providerType is not None, f"providerType missing: {b}"
    #         assert b.providerCode, f"providerCode is empty: {b}"
    #         assert b.isVerified is not None, f"isVerified missing: {b}"

    @allure.title("GET /Accounts/sso without auth — 401/403")
    @pytest.mark.ng
    def test_sso_bindings_401_without_auth(self):
        response = AccountsSsoBindingsAPI().get_sso_bindings_without_auth()

        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
