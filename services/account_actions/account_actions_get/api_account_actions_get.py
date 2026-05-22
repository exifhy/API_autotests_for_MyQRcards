from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_actions.account_actions_get.endpoints import Endpoints
from services.account_actions.account_actions_get.models.account_actions_get_model import (
    AccountActionItemModel,
    AccountActionsGetModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountActionsGetAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accountActions")
    def get_account_actions(self) -> tuple[requests.Response, AccountActionsGetModel]:
        return self.get_account_actions_by_token(bearer_token=get_token())

    @allure.step("GET /accountActions (by action token)")
    def get_account_actions_by_token(
        self, bearer_token: str, app_id: str | None = None
    ) -> tuple[requests.Response, AccountActionsGetModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_account_actions_endpoint,
            headers=Headers.auth_header(bearer_token=bearer_token, app_id=app_id),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.PARTIAL_CONTENT, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else []
        if isinstance(data, dict):
            raw_items = [data]
        elif isinstance(data, list):
            raw_items = [item for item in data if isinstance(item, dict)]
        else:
            raw_items = []
        return response, AccountActionsGetModel(
            items=[AccountActionItemModel(**item) for item in raw_items],
            raw=raw_items,
        )
