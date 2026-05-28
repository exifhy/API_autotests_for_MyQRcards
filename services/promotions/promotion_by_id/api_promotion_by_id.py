from http import HTTPStatus

import allure

from config.headers import Headers
from services.promotions.promotion_by_id.endpoints import Endpoints
from services.promotions.promotion_by_id.models.promotion_by_id_model import PromotionByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class PromotionByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /promotions/{promotion_id}")
    def get_promotion_by_id(self, promotion_id: str) -> PromotionByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_promotion_by_id_endpoint.format(promotion_id=promotion_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert data.get("id") == promotion_id, (
            f"Expected promotion id {promotion_id}, got {data.get('id')}"
        )
        return PromotionByIdModel(**data)

