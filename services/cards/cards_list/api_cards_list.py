from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.cards.cards_list.endpoints import Endpoints
from services.cards.cards_list.models.cards_list_model import CardListItemModel, CardsListModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards")
    def get_cards(
        self,
        *,
        range_header: str | None = 'items=0-199',
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params['offset'] = str(offset)
        if fetch is not None:
            params['fetch'] = str(fetch)

        headers = Headers.auth_header(bearer_token=get_token())
        if range_header:
            headers['Range'] = range_header

        response = None
        last_error = None
        for attempt in range(4):
            try:
                response = self._call(
                    "GET",
                    url=self.endpoints.get_cards_endpoint,
                    headers=headers,
                    params=params or None,
                )
                if response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                    break
            except requests.RequestException as error:
                last_error = error
                response = None
            if attempt < 3:
                time.sleep(2)

        if response is None and last_error is not None:
            raise last_error
        assert response is not None
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardsListModel(items=items)

    @allure.step("GET /Cards without auth")
    def get_cards_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_cards_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
