from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_leadgen_forms_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardLeadGenFormsDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Accounts/{account_id}/Cards/{card_id}/leadGenForms")
    def delete_accounts_card_leadgen_forms(self, account_id: int, card_id: int, leadgen_form_ids: list[int]):
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_accounts_card_leadgen_forms_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=leadgen_form_ids,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response
