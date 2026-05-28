from http import HTTPStatus

import allure
import requests

from services.cardlinks.cardlink_download_v2.endpoints import Endpoints
from services.cardlinks.cardlink_download_v2.models.cardlink_download_v2_model import (
    CardLinkDownloadV2Model,
)
from src.support.helper import Helper


class CardLinkDownloadV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardLinks/{card_link}/card/download/V2")
    def get_cardlink_download_v2(self, card_link: str) -> tuple[requests.Response, CardLinkDownloadV2Model]:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_download_v2_endpoint.format(card_link=card_link),
            headers={"Accept": "*/*"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        content_type = response.headers.get("content-type", "")
        body_text = response.text if response.text else ""
        model = CardLinkDownloadV2Model(
            content_type=content_type,
            is_vcard=body_text.startswith("BEGIN:VCARD"),
            body_text=body_text,
        )
        return response, model
