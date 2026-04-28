from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_leadgen_forms_create.endpoints import Endpoints
from services.cards.card_leadgen_forms_create.models.card_leadgen_forms_create_model import (
    CardLeadGenFormsCreateModel,
)
from services.cards.card_leadgen_forms_create.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLeadGenFormsCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Cards/{card_id}/leadGenForms")
    def create_card_leadgen_form(
        self,
        card_id: int,
        *,
        field_template_id: int,
        custom_message_template_id: int | None = None,
    ) -> CardLeadGenFormsCreateModel:
        payload = Payloads.build_card_leadgen_form_create_payload(
            field_template_id=field_template_id,
            custom_message_template_id=custom_message_template_id,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_card_leadgen_form_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return CardLeadGenFormsCreateModel(**response.json())

