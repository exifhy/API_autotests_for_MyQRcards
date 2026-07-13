from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_list.endpoints import Endpoints
from services.accounts.accounts_list.models.accounts_list_model import AccountListItemModel, AccountsListModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts")
    def get_accounts(
        self,
        range_header: str = "items=0-199",
        *,
        account_id: int | None = None,
        company_id: int | None = None,
        include_subscription_owner: bool | None = None,
    ) -> tuple[requests.Response, AccountsListModel]:
        params: dict[str, str] = {}
        if account_id is not None:
            params["accountID"] = str(account_id)
        if company_id is not None:
            params["companyID"] = str(company_id)
        if include_subscription_owner is not None:
            params["IsIncludeSubscriptionOwner"] = str(include_subscription_owner).lower()

        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_list_endpoint,
            headers=Headers.auth_header(bearer_token=get_token(), Range=range_header),
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT, HTTPStatus.NO_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [AccountListItemModel(id=item.get("id"), email=item.get("email")) for item in data if isinstance(item, dict)]
        return response, AccountsListModel(items=items)

    @allure.step("GET /accounts without auth")
    def get_accounts_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_list_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
