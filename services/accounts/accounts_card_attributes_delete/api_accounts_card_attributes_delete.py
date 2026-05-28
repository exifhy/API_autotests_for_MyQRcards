from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_attributes_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardAttributesDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /accounts/{account_id}/cards/{card_id}/attributes")
    def delete_accounts_card_attributes(
        self,
        account_id: int,
        card_id: int,
        attribute_ids: list[int],
    ) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_accounts_card_attributes_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=[int(aid) for aid in attribute_ids],
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), f"Expected 200/202/204/404, got {response.status_code}: {response.text}"
        return response

    @allure.step("DELETE /accounts/{account_id}/cards/{card_id}/attributes without auth")
    def delete_accounts_card_attributes_without_auth(self, account_id: int, card_id: int) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_accounts_card_attributes_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.without_authorization_field_header(),
            json=[1],
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
