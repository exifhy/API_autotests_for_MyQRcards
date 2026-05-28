from http import HTTPStatus

import allure

from config.headers import Headers
from services.attachments.attachment_delete_by_id.endpoints import Endpoints
from services.attachments.attachment_delete_by_id.models.attachment_delete_by_id_model import AttachmentDeleteByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttachmentDeleteByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Attachments/{attachment_id}")
    def delete_attachment_by_id(self, attachment_id: int) -> AttachmentDeleteByIdModel:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_attachment_by_id_endpoint.format(attachment_id=int(attachment_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return AttachmentDeleteByIdModel(status_code=response.status_code)
