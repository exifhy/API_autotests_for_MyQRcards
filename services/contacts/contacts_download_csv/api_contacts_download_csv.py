from __future__ import annotations

from http import HTTPStatus

import allure
import requests

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contacts_download_csv.endpoints import Endpoints
from services.contacts.contacts_download_csv.models.contacts_download_csv_model import (
    ContactsDownloadCsvModel,
)
from src.support.helper import Helper


class ContactsDownloadCsvAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/contacts/download")
    def download_contacts_csv(self, *, app_id: str | None = None) -> tuple[requests.Response, ContactsDownloadCsvModel]:
        response = self._call(
            "GET",
            url=self.endpoints.download_contacts_csv_endpoint,
            headers=self.build_headers(app_id=app_id, accept="*/*"),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        content_type = response.headers.get("Content-Type") or response.headers.get("content-type") or ""
        body_text = response.content.decode("utf-8-sig", errors="replace")
        return response, ContactsDownloadCsvModel(
            content_type=content_type,
            has_bom_utf8=response.content.startswith(b"\xef\xbb\xbf"),
            body_text=body_text,
        )
