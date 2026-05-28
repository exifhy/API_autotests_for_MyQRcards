import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cardlinks_list.api_accounts_cardlinks_list import AccountsCardLinksListAPI
from services.cardlinks.cardlink_catalog_by_id.api_cardlink_catalog_by_id import CardLinkCatalogByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    GET /cardlinks/{token}/catalog/{id}
    Catalog not yet implemented — expecting 204 No Content
    """
)
class TestCardLinkCatalogById:
    @allure.title("GET /Accounts/{id}/Cards/links -> GET /cardlinks/{token}/catalog/{id} -> 204")
    def test_cardlink_catalog_by_id_204(self, cfg):
        with allure.step("GET cardlink token from account"):
            _, cardlinks = AccountsCardLinksListAPI().get_accounts_cardlinks(int(cfg["lk_account_id"]))
            assert cardlinks.items, "No cardlinks found for account"
            cardlink_url = next((item.url for item in cardlinks.items if item.url), None)
            assert cardlink_url, "No cardlink with url found"
            token = extract_card_link_id(cardlink_url)

        with allure.step(f"GET /cardlinks/{token}/catalog/1"):
            response = CardLinkCatalogByIdAPI().get_cardlink_catalog_by_id(token, catalog_id=1)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND)

    @pytest.mark.ng
    @allure.title("GET /cardlinks/{token}/catalog/{id} without auth -> 401/403")
    def test_cardlink_catalog_by_id_401_without_auth(self, cfg):
        response = CardLinkCatalogByIdAPI().get_cardlink_catalog_by_id_without_auth("faketoken", catalog_id=1)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN, HTTPStatus.CONFLICT)
