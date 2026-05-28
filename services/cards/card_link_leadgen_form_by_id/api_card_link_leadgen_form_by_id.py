from http import HTTPStatus

import allure
import requests

from services.cards.card_link_leadgen_form_by_id.endpoints import Endpoints
from services.cards.card_link_leadgen_forms.models.card_link_leadgen_forms_model import CardLinkLeadGenFormItemModel
from src.support.helper import Helper


class CardLinkLeadGenFormByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_link_id}/cardLink/leadGenForms/{form_id}")
    def get_card_link_leadgen_form_by_id(
        self,
        card_link_id: str,
        form_id: int,
    ) -> tuple[requests.Response, CardLinkLeadGenFormItemModel | None]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_link_leadgen_form_by_id_endpoint.format(
                card_link_id=card_link_id,
                form_id=int(form_id),
            ),
            headers={"Accept": "application/json"},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, None

        data = response.json()
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return response, CardLinkLeadGenFormItemModel(**data)
