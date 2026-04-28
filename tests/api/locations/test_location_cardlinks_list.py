import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cardlinks_list.api_accounts_cardlinks_list import AccountsCardLinksListAPI
from services.locations.location_cardlinks_list.api_location_cardlinks_list import LocationCardLinksListAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Locations")
@pytest.mark.api
@allure.description(
    """
    GET /cards/attributes/locations/cardlink/{cardLinkId}
    """
)
class TestLocationCardLinksList:
    @allure.title("GET /cards/attributes/locations/cardlink/{token}")
    def test_location_cardlinks_list_200(self, cfg):
        with allure.step("GET cardlink token from account"):
            _, cardlinks = AccountsCardLinksListAPI().get_accounts_cardlinks(int(cfg["lk_account_id"]))
            assert cardlinks.items, "No cardlinks found for account"
            cardlink_url = next((item.url for item in cardlinks.items if item.url), None)
            assert cardlink_url, "No cardlink with url found"
            card_link_id = extract_card_link_id(cardlink_url)

        with allure.step(f"GET /cards/attributes/locations/cardlink/{card_link_id}"):
            response, model = LocationCardLinksListAPI().get_location_cardlinks_list(card_link_id)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)
