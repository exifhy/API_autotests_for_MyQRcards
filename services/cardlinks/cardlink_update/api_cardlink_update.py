from http import HTTPStatus

import allure

from config.headers import Headers
from services.cardlinks.cardlink_update.endpoints import Endpoints
from services.cardlinks.cardlink_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinkUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /cardlinks/{card_link}")
    def update_cardlink(
        self,
        card_link: str,
        *,
        card_id: int,
        is_default: bool = True,
        allow_default_conflict: bool = False,
    ):
        payload = Payloads.build_cardlink_update_payload(
            card_link_id=card_link,
            card_id=card_id,
            is_default=is_default,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.update_cardlink_endpoint.format(card_link=card_link),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        if allow_default_conflict and (
            response.status_code == HTTPStatus.CONFLICT and "CardLinkIsDefault" in response.text
        ):
            return response, payload
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload
