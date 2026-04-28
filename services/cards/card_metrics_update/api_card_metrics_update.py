from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_metrics_update.endpoints import Endpoints
from services.cards.card_metrics_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardMetricsUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/metrics")
    def update_card_metrics(self, card_id: int, *, metric_type_id: int):
        payload = Payloads.build_card_metrics_update_payload(metric_type_id=metric_type_id)
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_metrics_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response

