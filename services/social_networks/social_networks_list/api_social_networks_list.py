from http import HTTPStatus

import allure

from services.social_networks.social_networks_list.endpoints import Endpoints
from services.social_networks.social_networks_list.models.social_networks_list_model import (
    SocialNetworkItemModel,
    SocialNetworksListModel,
)
from src.support.helper import Helper


class SocialNetworksListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /socialNetworks")
    def get_social_networks(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_social_networks_endpoint,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        items = [SocialNetworkItemModel(**item) for item in data if isinstance(item, dict)]
        assert items, f"Social networks payload is empty or invalid: {data}"
        return response, SocialNetworksListModel(items=items)

