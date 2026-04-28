import allure
import pytest
from http import HTTPStatus

from services.social_networks.social_networks_list.api_social_networks_list import (
    SocialNetworksListAPI,
)


@allure.epic("API")
@allure.feature("SocialNetworks")
@pytest.mark.api
@allure.description(
    """
    /socialNetworks
    """
)
class TestSocialNetworksList:
    @allure.title("GET /socialNetworks returns list")
    @pytest.mark.smoke
    def test_social_networks_list_200(self):
        response, model = SocialNetworksListAPI().get_social_networks()

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)
        assert model.items, "Expected non-empty social networks list"

        first_item = model.items[0]
        assert first_item.id is not None
        assert first_item.name is None or first_item.name != ""
        assert first_item.nameEn is None or first_item.nameEn != ""

        names = {item.nameEn for item in model.items if item.nameEn}
        assert "Telegram" in names
        assert "WhatsApp" in names
