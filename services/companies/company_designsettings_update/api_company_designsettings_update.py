from http import HTTPStatus

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_designsettings_update.endpoints import Endpoints


class CompanyDesignsettingsUpdateAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Companies/{company_id}/designsettings")
    def update_company_designsettings(self, company_id: int, payload: dict):
        return self._request(
            "PUT",
            self.endpoints.update_company_designsettings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT),
            json=payload,
        )
