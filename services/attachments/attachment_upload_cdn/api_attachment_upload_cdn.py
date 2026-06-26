from __future__ import annotations

import allure
import requests

from config.headers import Headers
from services.attachments.attachment_upload_cdn.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token
from src.utils.image_factory import GeneratedFile


class AttachmentUploadCdnAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /attachments/v2/ — CDN upload")
    def upload_attachment_cdn(self, generated: GeneratedFile) -> requests.Response:
        headers = Headers.auth_header(bearer_token=get_token())
        headers.pop("Content-Type", None)
        return self._call(
            "POST",
            url=self.endpoints.upload_cdn_endpoint,
            headers=headers,
            data={
                "Attachments.Index": "0",
                "Attachments[0].IsIgnorePossibleDuplication": "true",
            },
            files={"Attachments[0].File": (generated.filename, generated.data, generated.content_type)},
        )
