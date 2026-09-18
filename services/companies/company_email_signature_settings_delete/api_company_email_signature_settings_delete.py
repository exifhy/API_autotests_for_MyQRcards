from http import HTTPStatus

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_email_signature_settings_delete.endpoints import Endpoints


class CompanyEmailSignatureSettingsDeleteAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Companies/{company_id}/emailsignaturesettings")
    def delete_email_signature_settings(self, company_id: int):
        return self._request(
            "DELETE",
            self.endpoints.delete_company_email_signature_settings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT),
        )

    @allure.step("DELETE /Companies/{company_id}/emailsignaturesettings (raw, no assert — for negative cases)")
    def delete_email_signature_settings_raw(self, company_id: int):
        return self._call(
            "DELETE",
            url=self.endpoints.delete_company_email_signature_settings_endpoint.format(company_id=company_id),
            headers=self._request_headers(),
        )

    @allure.step("DELETE /Companies/{company_id}/emailsignaturesettings (without auth)")
    def delete_email_signature_settings_without_auth(self, company_id: int):
        return self._request(
            "DELETE",
            self.endpoints.delete_company_email_signature_settings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
