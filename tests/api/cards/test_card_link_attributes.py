import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cardlinks_list.api_accounts_cardlinks_list import AccountsCardLinksListAPI
from services.cards.card_link_attributes.api_card_link_attributes import CardLinkAttributesAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    GET /cards/{token}/cardLink/attributes
    """
)
class TestCardLinkAttributes:
    @allure.title("GET /Accounts/{id}/Cards/links -> GET /cards/{token}/cardLink/attributes")
    @pytest.mark.smoke
    def test_card_link_attributes_200(self, cfg):
        with allure.step("GET cardlink token from account"):
            _, cardlinks = AccountsCardLinksListAPI().get_accounts_cardlinks(int(cfg["lk_account_id"]))
            assert cardlinks.items, "No cardlinks found for account"
            cardlink_url = next((item.url for item in cardlinks.items if item.url), None)
            assert cardlink_url, "No cardlink with url found"
            token = extract_card_link_id(cardlink_url)

        with allure.step(f"GET /cards/{token}/cardLink/attributes"):
            response, model = CardLinkAttributesAPI().get_card_link_attributes(token)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)
