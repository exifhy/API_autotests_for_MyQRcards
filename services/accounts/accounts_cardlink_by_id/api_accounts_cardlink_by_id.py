from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_cardlink_by_id.endpoints import Endpoints
from services.cardlinks.cardlink_by_id.models.cardlink_by_id_model import CardLinkByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardLinkByIdAPI(Helper):
    # NOTE:
    # This endpoint is intentionally not covered by active tests right now.
    # On dev it does not behave like a normal GET and the real contract still
    # needs clarification from Postman/backend examples before we return it to
    # baseline coverage and Allure flows.
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/links/{card_link}")
    def get_accounts_cardlink_by_id(self, account_id: int, card_id: int, card_link: str) -> CardLinkByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_cardlink_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                card_link=card_link,
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return CardLinkByIdModel(**data)

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/links/{card_link} without auth")
    def get_accounts_cardlink_by_id_without_auth(self, account_id: int, card_id: int, card_link: str):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_cardlink_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                card_link=card_link,
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response
