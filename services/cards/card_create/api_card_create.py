from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_create.endpoints import Endpoints
from services.cards.card_create.models.card_create_model import CardCreateModel
from services.cards.card_create.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Cards")
    def create_card(self, *, subscription_id: int, company_id: int) -> CardCreateModel:
        payload = Payloads.build_card_create_payload(subscription_id=subscription_id, company_id=company_id)
        response = self._call(
            "POST",
            url=self.endpoints.create_card_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return CardCreateModel(**response.json())
