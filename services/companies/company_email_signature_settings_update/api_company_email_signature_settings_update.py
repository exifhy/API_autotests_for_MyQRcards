from http import HTTPStatus

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_email_signature_settings_update.endpoints import Endpoints


class CompanyEmailSignatureSettingsUpdateAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Companies/{company_id}/emailsignaturesettings")
    def update_email_signature_settings(self, company_id: int, payload: dict):
        return self._request(
            "PUT",
            self.endpoints.update_company_email_signature_settings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT),
            json=payload,
        )

    @allure.step("PUT /Companies/{company_id}/emailsignaturesettings (raw, no assert — for negative cases)")
    def update_email_signature_settings_raw(self, company_id: int, payload: dict):
        return self._call(
            "PUT",
            url=self.endpoints.update_company_email_signature_settings_endpoint.format(company_id=company_id),
            headers=self._request_headers(),
            json=payload,
        )

    @allure.step("PUT /Companies/{company_id}/emailsignaturesettings (without auth)")
    def update_email_signature_settings_without_auth(self, company_id: int, payload: dict):
        return self._request(
            "PUT",
            self.endpoints.update_company_email_signature_settings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
