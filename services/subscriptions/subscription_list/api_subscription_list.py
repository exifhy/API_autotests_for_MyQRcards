import time
from datetime import datetime
from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_list.endpoints import Endpoints
from services.subscriptions.subscription_list.models.subscription_list_model import (
    SubscriptionListItemModel,
    SubscriptionListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @staticmethod
    def build_params(
        *,
        date_from: str,
        date_till: str,
        account_id: int | None = None,
        company_id: int | None = None,
    ) -> dict[str, str]:
        params = {
            "DateFrom": date_from,
            "DateTill": date_till,
        }
        if account_id is not None:
            params["accountID"] = str(account_id)
        if company_id is not None:
            params["companyID"] = str(company_id)
        return params

    @staticmethod
    def current_date_till() -> str:
        return datetime.now().strftime("%Y-%m-%dT23:59:59")

    @allure.step("GET /Subscriptions")
    def get_subscriptions(
        self,
        *,
        date_from: str,
        date_till: str,
        account_id: int | None = None,
        company_id: int | None = None,
    ) -> tuple[requests.Response, SubscriptionListModel]:
        params = self.build_params(
            date_from=date_from,
            date_till=date_till,
            account_id=account_id,
            company_id=company_id,
        )
        response = self._call(
            "GET",
            url=self.endpoints.get_subscriptions_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND), (
            f"Expected 200/404, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NOT_FOUND or not response.text:
            return response, SubscriptionListModel(items=[], raw=[])
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        return response, SubscriptionListModel(
            items=[SubscriptionListItemModel(**item) for item in data if isinstance(item, dict)],
            raw=[item for item in data if isinstance(item, dict)],
        )
