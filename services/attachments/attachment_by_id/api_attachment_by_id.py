from http import HTTPStatus

import allure

from config.headers import Headers
from services.attachments.attachment_by_id.endpoints import Endpoints
from services.attachments.attachment_by_id.models.attachment_by_id_model import AttachmentByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttachmentByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Attachments/{attachment_id}")
    def get_attachment_by_id(self, attachment_id: int) -> AttachmentByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_attachment_by_id_endpoint.format(attachment_id=int(attachment_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return AttachmentByIdModel(**response.json())
