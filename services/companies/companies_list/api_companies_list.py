from http import HTTPStatus

import allure

from config.headers import Headers
from services.companies.base_api import CompaniesBaseAPI
from services.companies.companies_list.endpoints import Endpoints
from services.companies.companies_list.models.companies_list_model import (
    CompaniesListModel,
    CompanyListItemModel,
)
from src.support.token_utils import get_token


class CompaniesListAPI(CompaniesBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Companies")
    def get_companies(
        self,
        *,
        range_header: str = "items=0-199",
        search_text: str | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if search_text:
            params["searchText"] = search_text
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        response = self._request(
            "GET",
            self.endpoints.get_companies_list_endpoint,
            expected_statuses=(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT),
            headers=Headers.auth_header(bearer_token=get_token(), Range=range_header),
            params=params or None,
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CompanyListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CompaniesListModel(items=items)

    @allure.step("GET /Companies without auth")
    def get_companies_without_auth(self):
        response = self._request(
            "GET",
            self.endpoints.get_companies_list_endpoint,
            expected_statuses=(HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            headers=Headers.without_authorization_field_header(),
        )
        return response
