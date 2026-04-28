from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.powerbi_reports.powerbi_report_by_id.endpoints import Endpoints
from services.powerbi_reports.powerbi_report_by_id.models.powerbi_report_by_id_model import PowerBIReportByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class PowerBIReportByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /powerbireports/{report_id}")
    def get_powerbi_report_by_id(
        self,
        report_id: int,
    ) -> tuple[requests.Response, PowerBIReportByIdModel | None]:
        response = self._call(
            "GET",
            url=self.endpoints.get_powerbi_report_by_id_endpoint.format(report_id=int(report_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND), (
            f"Expected 200/204/404, got {response.status_code}: {response.text}"
        )

        if response.status_code != HTTPStatus.OK or not response.text:
            return response, None

        data = response.json()
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return response, PowerBIReportByIdModel(**data)

    @allure.step("GET /powerbireports/{report_id} without auth")
    def get_powerbi_report_by_id_without_auth(self, report_id: int) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_powerbi_report_by_id_endpoint.format(report_id=int(report_id)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
