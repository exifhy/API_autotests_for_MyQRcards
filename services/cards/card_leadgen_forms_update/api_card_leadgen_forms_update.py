from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_leadgen_forms_update.endpoints import Endpoints
from services.cards.card_leadgen_forms_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLeadGenFormsUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/leadGenForms")
    def update_card_leadgen_forms(
        self,
        card_id: int,
        *,
        leadgen_form_id: int,
        field_template_id: int,
        custom_message_template_id: int | None = None,
    ):
        payload = Payloads.build_card_leadgen_forms_update_payload(
            leadgen_form_id=leadgen_form_id,
            field_template_id=field_template_id,
            custom_message_template_id=custom_message_template_id,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_leadgen_forms_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload

