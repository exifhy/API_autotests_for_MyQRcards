from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.cards_list_v2.endpoints import Endpoints
from services.cards.cards_list_v2.models.cards_list_v2_model import CardV2ListItemModel, CardsListV2Model
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardsListV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/v2.0")
    def get_cards_v2(
        self,
        *,
        range_header: str | None = 'items=0-199',
        offset: int | None = None,
        fetch: int | None = None,
        all_data: bool | None = True,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params['offset'] = str(offset)
        if fetch is not None:
            params['fetch'] = str(fetch)
        if all_data is not None:
            params['AllData'] = str(all_data).lower()

        headers = Headers.auth_header(bearer_token=get_token())
        if range_header:
            headers['Range'] = range_header

        response = self._call(
            "GET",
            url=self.endpoints.get_cards_v2_endpoint,
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardV2ListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardsListV2Model(items=items)

    @allure.step("GET /Cards/v2.0 without auth")
    def get_cards_v2_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_cards_v2_endpoint,
            headers=Headers.without_authorization_field_header(),
            params={'AllData': 'true'},
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
