from http import HTTPStatus

import allure

from services.leadgen.leadgen_form_fields.endpoints import Endpoints
from services.leadgen.leadgen_form_fields.models.leadgen_form_fields_model import (
    LeadGenFormFieldItemModel,
    LeadGenFormFieldsModel,
)
from src.support.helper import Helper


class LeadGenFormFieldsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /LeadGenFormFields")
    def get_leadgen_form_fields(
        self,
        *,
        range_header: str = "items=0-199",
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        headers = {
            "Accept": "application/json",
            "Range": range_header,
        }

        response = self._call(
            "GET",
            url=self.endpoints.get_leadgen_form_fields_endpoint,
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [LeadGenFormFieldItemModel(**item) for item in data if isinstance(item, dict)]
        return response, LeadGenFormFieldsModel(items=items)

