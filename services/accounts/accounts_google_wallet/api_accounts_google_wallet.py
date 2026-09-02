from http import HTTPStatus
from typing import Optional

import allure

from config.headers import Headers
from services.accounts.accounts_google_wallet.endpoints import Endpoints
from services.accounts.accounts_google_wallet.models.google_wallet_result_model import (
    GoogleWalletResultModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsGoogleWalletAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/GoogleWallet/{card_id}")
    def create_google_wallet(self, card_id: int) -> Optional[GoogleWalletResultModel]:
        response = self._call(
            "POST",
            url=self.endpoints.create_google_wallet_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200 or 204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT:
            return None
        return GoogleWalletResultModel(**response.json())

    @allure.step("POST /Accounts/GoogleWallet/{card_id} (raw, no assert — for negative cases)")
    def create_google_wallet_raw(self, card_id):
        return self._call(
            "POST",
            url=self.endpoints.create_google_wallet_endpoint.format(card_id=card_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )

    @allure.step("POST /Accounts/GoogleWallet/{card_id} (without auth)")
    def create_google_wallet_without_auth(self, card_id: int):
        return self._call(
            "POST",
            url=self.endpoints.create_google_wallet_endpoint.format(card_id=int(card_id)),
            headers=Headers.without_authorization_field_header(),
        )
