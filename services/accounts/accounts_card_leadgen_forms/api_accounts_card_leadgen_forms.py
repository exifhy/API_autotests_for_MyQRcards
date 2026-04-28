from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_leadgen_forms.endpoints import Endpoints
from services.cards.card_leadgen_forms.models.card_leadgen_forms_model import (
    CardLeadGenFormItemModel,
    CardLeadGenFormsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardLeadGenFormsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/leadGenForms")
    def get_accounts_card_leadgen_forms(
        self,
        account_id: int,
        card_id: int,
        *,
        range_header: str | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        headers = Headers.auth_header(bearer_token=get_token())
        if range_header:
            headers["Range"] = range_header

        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_leadgen_forms_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardLeadGenFormItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardLeadGenFormsModel(items=items)

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/leadGenForms without auth")
    def get_accounts_card_leadgen_forms_without_auth(self, account_id: int, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_leadgen_forms_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response
