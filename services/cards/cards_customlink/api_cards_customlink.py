from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.cards_customlink.endpoints import Endpoints
from services.cards.cards_customlink.models.cards_customlink_model import (
    CardCustomLinkItemModel,
    CardsCustomLinkModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardsCustomLinkAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/customlink")
    def get_cards_customlink(
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

        response = self._call(
            "GET",
            url=self.endpoints.get_cards_customlink_endpoint,
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardCustomLinkItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardsCustomLinkModel(items=items)

    @allure.step("GET /Cards/customlink without auth")
    def get_cards_customlink_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_cards_customlink_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
