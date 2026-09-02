from http import HTTPStatus
from typing import Optional

import allure

from services.accounts.accounts_google_wallet.models.google_wallet_result_model import (
    GoogleWalletResultModel,
)
from services.accounts.accounts_google_wallet_by_link.endpoints import Endpoints
from src.support.helper import Helper


class AccountsGoogleWalletByLinkAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/GoogleWallet/{card_link}/card (public, no auth)")
    def create_google_wallet_by_link(self, card_link: str) -> Optional[GoogleWalletResultModel]:
        response = self._call(
            "POST",
            url=self.endpoints.create_google_wallet_by_link_endpoint.format(card_link=card_link),
            headers={"Accept": "application/json"},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200 or 204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT:
            return None
        return GoogleWalletResultModel(**response.json())

    @allure.step("POST /Accounts/GoogleWallet/{card_link}/card (raw, no assert — for negative cases)")
    def create_google_wallet_by_link_raw(self, card_link):
        return self._call(
            "POST",
            url=self.endpoints.create_google_wallet_by_link_endpoint.format(card_link=card_link),
            headers={"Accept": "application/json"},
        )
