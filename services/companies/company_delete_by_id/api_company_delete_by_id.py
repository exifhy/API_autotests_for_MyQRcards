from http import HTTPStatus

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_delete_by_id.endpoints import Endpoints


class CompanyDeleteByIdAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Companies/{company_id}")
    def delete_company_by_id(self, company_id: int):
        return self._request(
            "DELETE",
            self.endpoints.delete_company_by_id_endpoint.format(company_id=company_id),
            expected_statuses=(
                HTTPStatus.OK,
                HTTPStatus.ACCEPTED,
                HTTPStatus.NO_CONTENT,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.FORBIDDEN,
            ),
        )
