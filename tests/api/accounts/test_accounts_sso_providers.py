import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_sso_providers.api_sso_providers import AccountsSsoProvidersAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    GET /Accounts/sso/providers
    300 — публичный справочник доступных SSO-провайдеров (Яндекс ID, VK ID).
    Ожидаемые провайдеры: Yandex (providerType=1), Vk (providerType=2).
    При отсутствии записей в справочнике возвращает 204.
    """
)
class TestAccountsSsoProviders:
    @allure.title("GET /Accounts/sso/providers — returns list of SSO providers")
    @pytest.mark.smoke
    def test_sso_providers_200(self):
        response, providers = AccountsSsoProvidersAPI().get_sso_providers()

        assert response.status_code == HTTPStatus.OK, (
            "Expected 200 with providers list, got 204 (no providers in DB)"
        )
        assert providers, "Expected non-empty providers list"

        codes = {p.code for p in providers}
        assert codes & {"Yandex", "Vk"}, (
            f"Expected at least one of Yandex/Vk providers, got: {codes}"
        )

    @allure.title("GET /Accounts/sso/providers — each provider has required fields")
    def test_sso_providers_structure(self):
        response, providers = AccountsSsoProvidersAPI().get_sso_providers()

        if response.status_code == HTTPStatus.NO_CONTENT:
            pytest.skip("No SSO providers in DB (204 response)")

        for p in providers:
            assert p.providerType is not None, f"providerType missing: {p}"
            assert p.code, f"code is empty: {p}"
            assert p.nameRu, f"nameRu is empty: {p}"
            assert p.nameEn, f"nameEn is empty: {p}"

    @allure.title("GET /Accounts/sso/providers — public endpoint, no auth required")
    @pytest.mark.ng
    def test_sso_providers_public_no_auth(self):
        response = AccountsSsoProvidersAPI().get_sso_providers_without_auth()
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200 or 204 (public endpoint), got {response.status_code}: {response.text}"
        )
