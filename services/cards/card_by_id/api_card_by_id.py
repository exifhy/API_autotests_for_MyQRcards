from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.cards.card_by_id.endpoints import Endpoints
from services.cards.card_by_id.models.card_by_id_model import CardByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}")
    def get_card_by_id(self, card_id: int) -> CardByIdModel:
        response = None
        last_error = None
        for attempt in range(5):
            try:
                response = self._call(
                    "GET",
                    url=self.endpoints.get_card_by_id_endpoint.format(card_id=int(card_id)),
                    headers=Headers.auth_header(bearer_token=get_token()),
                )
                if response.status_code == HTTPStatus.OK:
                    break
                if response.status_code not in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND):
                    break
            except requests.RequestException as error:
                last_error = error
                response = None
            if attempt < 4:
                time.sleep(2)
        if response is None and last_error is not None:
            raise last_error
        assert response is not None
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return CardByIdModel(**response.json())
