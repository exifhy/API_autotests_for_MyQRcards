from http import HTTPStatus

import allure

from config.headers import Headers
from services.cardlinks.cardlinks_statistic.endpoints import Endpoints
from services.cardlinks.cardlinks_statistic.models.cardlinks_statistic_model import (
    CardLinksStatisticItemModel,
    CardLinksStatisticModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinksStatisticAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardlinks/statistic")
    def get_cardlinks_statistic(
        self,
        *,
        date_from: str,
        date_till: str,
        account_id: int | None = None,
        company_id: int | None = None,
    ):
        params = {
            "DateFrom": date_from,
            "DateTill": date_till,
        }
        if account_id is not None:
            params["accountID"] = str(account_id)
        if company_id is not None:
            params["companyID"] = str(company_id)

        response = self._call(
            "GET",
            url=self.endpoints.get_cardlinks_statistic_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardLinksStatisticItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardLinksStatisticModel(items=items)
