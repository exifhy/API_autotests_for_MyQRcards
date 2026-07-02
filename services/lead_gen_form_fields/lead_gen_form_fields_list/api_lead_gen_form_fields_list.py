from http import HTTPStatus

import allure

from config.headers import Headers
from services.lead_gen_form_fields.lead_gen_form_fields_list.endpoints import Endpoints
from services.lead_gen_form_fields.lead_gen_form_fields_list.models.lead_gen_form_fields_model import (
    LeadGenFormFieldModel,
)
from src.support.helper import Helper


class LeadGenFormFieldsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /LeadGenFormFields")
    def get_lead_gen_form_fields(self) -> list[LeadGenFormFieldModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_lead_gen_form_fields_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}: {data}"
        return [LeadGenFormFieldModel(**item) for item in data]
