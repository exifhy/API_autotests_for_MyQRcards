from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.powerbi_reports.powerbi_reports_list.endpoints import Endpoints
from services.powerbi_reports.powerbi_reports_list.models.powerbi_reports_list_model import (
    PowerBIReportItemModel,
    PowerBIReportsListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class PowerBIReportsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /powerbireports/")
    def get_powerbi_reports(self) -> tuple[requests.Response, PowerBIReportsListModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_powerbi_reports_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, PowerBIReportsListModel(items=[])

        data = response.json()
        if isinstance(data, list):
            items = [PowerBIReportItemModel(**item) for item in data if isinstance(item, dict)]
        else:
            items = []
        return response, PowerBIReportsListModel(items=items)

    @allure.step("GET /powerbireports/ without auth")
    def get_powerbi_reports_without_auth(self) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_powerbi_reports_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
