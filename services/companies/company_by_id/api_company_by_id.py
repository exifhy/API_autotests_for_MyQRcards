from http import HTTPStatus

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_by_id.endpoints import Endpoints
from services.companies.company_by_id.models.company_by_id_model import CompanyByIdModel


class CompanyByIdAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Companies/{company_id}")
    def get_company_by_id(self, company_id: int) -> CompanyByIdModel:
        response = self._request(
            "GET",
            self.endpoints.get_company_by_id_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.OK,),
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert int(data["id"]) == int(company_id), (
            f"Expected company id={company_id}, got {data.get('id')}"
        )
        return CompanyByIdModel(**data)
