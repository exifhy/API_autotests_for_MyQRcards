from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_leadgen_forms_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLeadGenFormsDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Cards/{card_id}/leadGenForms")
    def delete_card_leadgen_forms(self, card_id: int, leadgen_form_ids: list[int]):
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_card_leadgen_forms_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=leadgen_form_ids,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response

