from http import HTTPStatus

import allure

from services.promotions.promotions_list.endpoints import Endpoints
from services.promotions.promotions_list.models.promotions_list_model import (
    PromotionListItemModel,
    PromotionsListModel,
)
from src.support.helper import Helper


class PromotionsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /promotions")
    def get_promotions(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_promotions_endpoint,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, PromotionsListModel(items=[])

        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        items = [PromotionListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, PromotionsListModel(items=items)

