from http import HTTPStatus
import time

import allure
import requests

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_create.endpoints import Endpoints
from services.companies.company_create.models.company_create_model import CompanyCreateModel


class CompanyCreateAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Companies")
    def create_company(self, payload: dict):
        response = None
        for attempt in range(3):
            response = self._call(
                "POST",
                url=self.endpoints.create_company_endpoint,
                headers=self._request_headers(),
                json=payload,
            )
            if response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
                break
            if response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR or "deadlock" not in response.text.lower():
                break
            if attempt < 2:
                time.sleep(2)
        assert response is not None
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        company_id = data.get("id") or data.get("companyID") or data.get("CompanyID")
        assert company_id, f"No company id in response: {data}"
        return response, CompanyCreateModel(id=int(company_id))
