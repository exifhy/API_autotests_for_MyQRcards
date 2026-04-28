from http import HTTPStatus

import allure

from config.headers import Headers
from services.metrics.metric_types.endpoints import Endpoints
from services.metrics.metric_types.models.metric_types_model import (
    MetricTypeItemModel,
    MetricTypesModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class MetricTypesAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /MetricTypes")
    def get_metric_types(
        self,
        *,
        range_header: str = "items=0-199",
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        response = self._call(
            "GET",
            url=self.endpoints.get_metric_types_endpoint,
            headers=Headers.auth_header(bearer_token=get_token(), Range=range_header),
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [MetricTypeItemModel(**item) for item in data if isinstance(item, dict)]
        return response, MetricTypesModel(items=items)

    @allure.step("GET /MetricTypes without auth")
    def get_metric_types_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_metric_types_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response

