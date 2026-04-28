from http import HTTPStatus

import allure
import requests

from services.cardlinks.cardlink_download.endpoints import Endpoints
from services.cardlinks.cardlink_download.models.cardlink_download_model import (
    CardLinkDownloadModel,
)
from src.support.helper import Helper


class CardLinkDownloadAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardLinks/{card_link}/card/download")
    def get_cardlink_download(self, card_link: str) -> tuple[requests.Response, CardLinkDownloadModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_download_endpoint.format(card_link=card_link),
            headers={"Accept": "*/*"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        content_type = response.headers.get("content-type", "")
        body_text = response.text if response.text else ""
        model = CardLinkDownloadModel(
            content_type=content_type,
            is_vcard=body_text.startswith("BEGIN:VCARD"),
            body_text=body_text,
        )
        return response, model
