from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_employments_list.endpoints import Endpoints
from services.accounts.accounts_employments_list.models.accounts_employments_list_model import (
    AccountsEmploymentItemModel,
    AccountsEmploymentsListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsEmploymentsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/{account_id}/employments")
    def get_accounts_employments(self, account_id: int) -> tuple[requests.Response, AccountsEmploymentsListModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_employments_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        raw_items = [item for item in data.values() if isinstance(item, dict)]
        return response, AccountsEmploymentsListModel(
            items=[AccountsEmploymentItemModel(**item) for item in raw_items],
            raw=raw_items,
        )
