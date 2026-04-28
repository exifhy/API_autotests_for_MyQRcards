import allure
import pytest
from http import HTTPStatus

from services.locations.location_by_id.api_location_by_id import LocationByIdAPI


@allure.epic("API")
@allure.feature("Locations")
@pytest.mark.api
@allure.description(
    """
    /Locations/{id}
    """
)
class TestLocationById:
    @allure.title("GET /Locations/{id} returns location data")
    @pytest.mark.smoke
    def test_get_location_by_id_200(self):
        location_id = 1

        model = LocationByIdAPI().get_location_by_id(location_id)

        assert model.id == location_id
        assert model.country is None or model.country != ""
        assert model.address is None or model.address != ""

    @allure.title("GET /Locations/{id} without auth")
    @pytest.mark.ng
    def test_get_location_by_id_401_without_auth(self):
        response = LocationByIdAPI().get_location_by_id_without_auth(1)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

