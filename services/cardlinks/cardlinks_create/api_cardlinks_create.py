from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cardlinks.cardlinks_create.endpoints import Endpoints
from services.cardlinks.cardlinks_create.models.cardlinks_create_model import CardLinksCreateModel
from services.cardlinks.cardlinks_create.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinksCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /cards/{card_id}/links")
    def create_cardlink(
        self,
        card_id: int,
        *,
        custom_cardlink_id: str,
        is_default: bool = False,
        payload: dict | None = None,
    ) -> tuple[requests.Response, CardLinksCreateModel, dict]:
        request_payload = payload or Payloads.build_cardlinks_create_payload(
            custom_cardlink_id=custom_cardlink_id,
            is_default=is_default,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_cardlinks_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return response, CardLinksCreateModel(**response.json()), request_payload
