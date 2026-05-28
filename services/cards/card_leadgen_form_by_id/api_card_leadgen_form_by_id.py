from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_leadgen_form_by_id.endpoints import Endpoints
from services.cards.card_leadgen_form_by_id.models.card_leadgen_form_by_id_model import (
    CardLeadGenFormByIdModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLeadGenFormByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/leadGenForms/{leadgen_form_id}")
    def get_card_leadgen_form_by_id(self, card_id: int, leadgen_form_id: int) -> CardLeadGenFormByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_leadgen_form_by_id_endpoint.format(
                card_id=int(card_id),
                leadgen_form_id=int(leadgen_form_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert int(data["cardID"]) == int(card_id), (
            f"Expected cardID={card_id}, got {data.get('cardID')}"
        )
        assert int(data["id"]) == int(leadgen_form_id), (
            f"Expected leadGenFormID={leadgen_form_id}, got {data.get('id')}"
        )
        return CardLeadGenFormByIdModel(**data)

    @allure.step("GET /Cards/{card_id}/leadGenForms/{leadgen_form_id} without auth")
    def get_card_leadgen_form_by_id_without_auth(self, card_id: int, leadgen_form_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_card_leadgen_form_by_id_endpoint.format(
                card_id=int(card_id),
                leadgen_form_id=int(leadgen_form_id),
            ),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

