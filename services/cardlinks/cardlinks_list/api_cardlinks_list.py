from http import HTTPStatus
import time

import allure
import requests

from services.cardlinks.cardlinks_list.endpoints import Endpoints
from services.cardlinks.cardlinks_list.models.cardlinks_list_model import (
    CardLinksListItemModel,
    CardLinksListModel,
)
from src.support.helper import Helper


class CardLinksListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardLinks")
    def get_cardlinks(self, *, account_uri_name: str):
        response = None
        last_error = None
        for attempt in range(4):
            try:
                response = self._call(
                    "GET",
                    url=self.endpoints.get_cardlinks_endpoint,
                    headers={"Accept": "file/json"},
                    params={"accountUriName": account_uri_name},
                )
                if response.status_code == HTTPStatus.OK:
                    break
                if attempt < 3:
                    time.sleep(2)
            except requests.RequestException as error:
                last_error = error
                if attempt < 3:
                    time.sleep(2)
                    continue
                raise
        if response is None and last_error is not None:
            raise last_error
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardLinksListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardLinksListModel(items=items)
