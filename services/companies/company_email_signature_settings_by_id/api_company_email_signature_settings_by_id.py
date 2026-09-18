from http import HTTPStatus
from typing import Optional

import allure

from services.companies.base_api import CompaniesBaseAPI
from services.companies.company_email_signature_settings_by_id.endpoints import Endpoints
from services.companies.company_email_signature_settings_by_id.models.company_email_signature_settings_model import (
    CompanyEmailSignatureSettingsModel,
)


class CompanyEmailSignatureSettingsByIdAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Companies/{company_id}/emailsignaturesettings")
    def get_email_signature_settings(self, company_id: int) -> Optional[CompanyEmailSignatureSettingsModel]:
        response = self._request(
            "GET",
            self.endpoints.get_company_email_signature_settings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.OK, HTTPStatus.NO_CONTENT),
        )
        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return None
        return CompanyEmailSignatureSettingsModel(**response.json())

    @allure.step("GET /Companies/{company_id}/emailsignaturesettings (raw, no assert)")
    def get_email_signature_settings_raw(self, company_id: int):
        return self._call(
            "GET",
            url=self.endpoints.get_company_email_signature_settings_endpoint.format(company_id=company_id),
            headers=self._request_headers(),
        )

    @allure.step("GET /Companies/{company_id}/emailsignaturesettings (without auth)")
    def get_email_signature_settings_without_auth(self, company_id: int):
        return self._request(
            "GET",
            self.endpoints.get_company_email_signature_settings_endpoint.format(company_id=company_id),
            expected_statuses=(HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
