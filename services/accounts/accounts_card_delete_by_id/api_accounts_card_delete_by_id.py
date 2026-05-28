from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_delete_by_id.endpoints import Endpoints
from services.cards.card_delete_by_id.models.card_delete_by_id_model import CardDeleteByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardDeleteByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Accounts/{account_id}/Cards/{card_id}")
    def delete_accounts_card_by_id(self, account_id: int, card_id: int) -> CardDeleteByIdModel:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_accounts_card_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return CardDeleteByIdModel(status_code=response.status_code)

