from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_download_by_id.endpoints import Endpoints
from services.cards.card_download_by_id.models.card_download_by_id_model import CardDownloadByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardDownloadByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/download")
    def get_card_download_by_id(self, card_id: int) -> tuple[requests.Response, CardDownloadByIdModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_download_by_id_endpoint.format(card_id=int(card_id)),
            headers={
                'Authorization': f'Bearer {get_token()}',
                'Accept': '*/*',
            },
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        content_type = response.headers.get('content-type', '')
        body_text = response.text if response.text else ''
        model = CardDownloadByIdModel(
            content_type=content_type,
            is_vcard=body_text.startswith('BEGIN:VCARD'),
            body_text=body_text,
        )
        return response, model
