from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_copy.endpoints import Endpoints
from services.cards.card_copy.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardCopyAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /cards/card/copy")
    def copy_cards(self, *items: dict, allow_subscription_constraint: bool = False):
        payload = Payloads.build_card_copy_payload(*items)
        response = self._call(
            "POST",
            url=self.endpoints.card_copy_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        if (
            allow_subscription_constraint
            and response.status_code == HTTPStatus.FORBIDDEN
            and "SubscriptionConstraint" in response.text
        ):
            return response, payload
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return response, payload
