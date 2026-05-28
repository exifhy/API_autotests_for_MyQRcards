from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.cards.card_delete_by_id.endpoints import Endpoints
from services.cards.card_delete_by_id.models.card_delete_by_id_model import CardDeleteByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardDeleteByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Cards/{card_id}")
    def delete_card_by_id(self, card_id: int) -> CardDeleteByIdModel:
        response = None
        last_error = None
        for attempt in range(2):
            try:
                response = self._call(
                    "DELETE",
                    url=self.endpoints.delete_card_by_id_endpoint.format(card_id=int(card_id)),
                    headers=Headers.auth_header(bearer_token=get_token()),
                )
                break
            except requests.RequestException as error:
                last_error = error
                if attempt == 1:
                    raise
                time.sleep(1)

        if response is None:
            raise last_error or RuntimeError("Failed to delete card")
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return CardDeleteByIdModel(status_code=response.status_code)
