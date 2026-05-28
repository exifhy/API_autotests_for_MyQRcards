from http import HTTPStatus

import allure

from services.cards.card_link_metrics.endpoints import Endpoints
from services.cards.card_link_metrics.models.card_link_metrics_model import (
    CardLinkMetricItemModel,
    CardLinkMetricsModel,
)
from src.support.helper import Helper


class CardLinkMetricsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_link_id}/cardLink/metrics")
    def get_card_link_metrics(
        self,
        card_link_id: str,
        *,
        range_header: str | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        headers: dict[str, str] = {"Accept": "application/json"}
        if range_header:
            headers["Range"] = range_header

        response = self._call(
            "GET",
            url=self.endpoints.get_card_link_metrics_endpoint.format(card_link_id=card_link_id),
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardLinkMetricItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardLinkMetricsModel(items=items)

