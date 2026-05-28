from http import HTTPStatus

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_designsettings_by_id.endpoints import Endpoints
from services.companies.company_designsettings_by_id.models.company_designsettings_by_id_model import (
    CompanyDesignsettingsByIdModel,
)


class CompanyDesignsettingsByIdAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Companies/{company_id}/designsettings")
    def get_company_designsettings(self, company_id: int) -> CompanyDesignsettingsByIdModel:
        response = self._request(
            "GET",
            self.endpoints.get_company_designsettings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.OK,),
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert int(data["companyID"]) == int(company_id), (
            f"Expected companyID={company_id}, got {data.get('companyID')}"
        )
        return CompanyDesignsettingsByIdModel(**data)
