from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_metrics_update.endpoints import Endpoints
from services.accounts.accounts_card_metrics_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardMetricsUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Accounts/{account_id}/Cards/{card_id}/metrics")
    def update_accounts_card_metrics(self, account_id: int, card_id: int, *, metric_type_id: int):
        payload = Payloads.build_accounts_card_metrics_update_payload(metric_type_id=metric_type_id)
        response = None
        for attempt in range(5):
            response = self._call(
                "PUT",
                url=self.endpoints.update_accounts_card_metrics_endpoint.format(
                    account_id=int(account_id),
                    card_id=int(card_id),
                ),
                headers=Headers.auth_header(bearer_token=get_token()),
                json=payload,
            )
            if response.status_code == HTTPStatus.ACCEPTED:
                break
            if not (
                response.status_code == HTTPStatus.NOT_FOUND and "CardNotFound" in response.text
            ):
                break
            if attempt < 4:
                time.sleep(2)
        assert response is not None
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload
