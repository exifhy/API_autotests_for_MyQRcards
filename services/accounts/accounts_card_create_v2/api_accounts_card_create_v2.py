from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_create_v2.endpoints import Endpoints
from services.accounts.accounts_card_create_v2.payloads import Payloads
from services.cards.card_create.models.card_create_model import CardCreateModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardCreateV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/{account_id}/Cards/V2")
    def create_accounts_card_v2(
        self,
        account_id: int,
        *,
        subscription_id: int | None = None,
        payload: dict | None = None,
    ) -> tuple[requests.Response, CardCreateModel, dict]:
        request_payload = payload or Payloads.build_accounts_card_create_v2_payload(subscription_id=subscription_id)
        response = self._call(
            "POST",
            url=self.endpoints.create_accounts_card_v2_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return response, CardCreateModel(**response.json()), request_payload

