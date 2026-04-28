import allure
import pytest
from http import HTTPStatus

from services.locations.locations_list.api_locations_list import LocationsListAPI


@allure.epic("API")
@allure.feature("Locations")
@pytest.mark.api
@allure.description(
    """
    /Locations?locationID=1
    """
)
class TestLocationsList:
    @allure.title("GET /Locations with locationID returns location map")
    @pytest.mark.smoke
    def test_locations_list_returns_status_and_dict_contract(self):
        response, model = LocationsListAPI().get_locations_by_query_id(location_id=1)

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, dict)
        assert "1" in model.items, "Expected locationID=1 in response payload"
        assert model.items["1"].country is None or model.items["1"].country != ""
        assert model.items["1"].address is None or model.items["1"].address != ""

    @allure.title("GET /Locations without auth")
    @pytest.mark.ng
    def test_locations_list_401_without_auth(self):
        response = LocationsListAPI().get_locations_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
