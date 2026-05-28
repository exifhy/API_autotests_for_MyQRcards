from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_by_id.endpoints import Endpoints
from services.cards.card_by_id.models.card_by_id_model import CardByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}")
    def get_accounts_card_by_id(self, account_id: int, card_id: int) -> CardByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return CardByIdModel(**response.json())

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id} without auth")
    def get_accounts_card_by_id_without_auth(self, account_id: int, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

