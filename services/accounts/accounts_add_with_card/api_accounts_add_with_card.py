from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_add_with_card.endpoints import Endpoints
from services.accounts.accounts_add_with_card.models.accounts_add_with_card_model import (
    AccountsAddWithCardModel,
)
from services.accounts.accounts_add_with_card.payloads import Payloads
from src.support.helper import Helper


class AccountsAddWithCardAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts")
    def create_account_with_card(
        self,
        *,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountsAddWithCardModel, dict]:
        request_payload = payload or Payloads.build_accounts_add_with_card_payload()
        response = self._call(
            "POST",
            url=self.endpoints.create_account_with_card_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )

        raw_id = (response.text or "").strip().strip('"')
        assert raw_id.isdigit(), f"Expected numeric account id in response body, got: {response.text}"
        return response, AccountsAddWithCardModel(id=int(raw_id)), request_payload
