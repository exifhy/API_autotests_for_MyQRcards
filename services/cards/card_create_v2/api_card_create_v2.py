from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_create.models.card_create_model import CardCreateModel
from services.cards.card_create_v2.endpoints import Endpoints
from services.cards.card_create_v2.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardCreateV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Cards/V2.0")
    def create_card_v2(self, *, attachment_id: int | None = None) -> CardCreateModel:
        base_payload = Payloads.build_card_create_v2_payload(attachment_id=attachment_id)
        variants = [base_payload]

        if attachment_id is not None:
            variant = {
                **base_payload,
                "Person": {
                    **base_payload["Person"],
                    "Attachments": [{"id": int(attachment_id)}],
                },
            }
            variants.append(variant)

        last_response = None
        for payload in variants:
            response = self._call(
                "POST",
                url=self.endpoints.create_card_v2_endpoint,
                headers=Headers.auth_header(bearer_token=get_token()),
                json=payload,
            )
            last_response = response
            if response.status_code == HTTPStatus.CREATED:
                return CardCreateModel(**response.json())

        assert last_response is not None
        raise AssertionError(
            f"Expected HTTPStatus.CREATED, got {last_response.status_code}: {last_response.text}"
        )
