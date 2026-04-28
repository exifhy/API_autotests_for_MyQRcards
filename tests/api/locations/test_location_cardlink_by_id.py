import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cardlinks_list.api_accounts_cardlinks_list import AccountsCardLinksListAPI
from services.locations.location_cardlink_by_id.api_location_cardlink_by_id import LocationCardLinkByIdAPI
from services.locations.location_create.api_location_create import LocationCreateAPI
from services.locations.location_create.payloads import Payloads as LocationPayloads
from services.locations.locations_delete.api_locations_delete import LocationsDeleteAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Locations")
@pytest.mark.api
@allure.description(
    """
    GET /cards/attributes/locations/{locationId}/cardlink/{cardLinkId}
    """
)
class TestLocationCardLinkById:
    @allure.title("POST /Locations -> GET /cards/attributes/locations/{id}/cardlink/{token} -> DELETE")
    def test_location_cardlink_by_id_200(self, cfg):
        location_id = None
        try:
            with allure.step("GET cardlink token from account"):
                _, cardlinks = AccountsCardLinksListAPI().get_accounts_cardlinks(int(cfg["lk_account_id"]))
                assert cardlinks.items, "No cardlinks found for account"
                cardlink_url = next((item.url for item in cardlinks.items if item.url), None)
                assert cardlink_url, "No cardlink with url found"
                card_link_id = extract_card_link_id(cardlink_url)

            with allure.step("POST /Locations — create location"):
                _, created = LocationCreateAPI().create_location(LocationPayloads.build_location_create_payload())
                location_id = created.id

            with allure.step(f"GET /cards/attributes/locations/{location_id}/cardlink/{card_link_id}"):
                response, _ = LocationCardLinkByIdAPI().get_location_cardlink_by_id(location_id, card_link_id)

            assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)

        finally:
            if location_id is not None:
                try:
                    LocationsDeleteAPI().delete_locations([location_id])
                except Exception:
                    pass
