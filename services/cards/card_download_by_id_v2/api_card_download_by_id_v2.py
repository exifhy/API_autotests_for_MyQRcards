from http import HTTPStatus

import allure
import requests

from services.cards.card_download_by_id_v2.endpoints import Endpoints
from services.cards.card_download_by_id_v2.models.card_download_by_id_v2_model import CardDownloadByIdV2Model
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardDownloadByIdV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/download/V2")
    def get_card_download_by_id_v2(self, card_id: int) -> tuple[requests.Response, CardDownloadByIdV2Model]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_download_by_id_v2_endpoint.format(card_id=int(card_id)),
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
        model = CardDownloadByIdV2Model(
            content_type=content_type,
            is_vcard=body_text.startswith('BEGIN:VCARD'),
            body_text=body_text,
        )
        return response, model
