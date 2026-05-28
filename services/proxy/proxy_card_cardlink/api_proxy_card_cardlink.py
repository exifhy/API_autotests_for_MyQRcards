from http import HTTPStatus

import allure
import requests

from services.proxy.proxy_card_cardlink.endpoints import Endpoints
from src.support.helper import Helper


class ProxyCardCardLinkAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /proxy/card/cardlink/{token}")
    def get_proxy_card_cardlink(self, token: str) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_proxy_card_cardlink_endpoint.format(token=token),
            headers={"Accept": "application/json"},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )
        return response
