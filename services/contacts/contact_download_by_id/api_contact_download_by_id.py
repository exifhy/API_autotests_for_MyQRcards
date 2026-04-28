from __future__ import annotations

from http import HTTPStatus

import allure
import requests

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contact_download_by_id.endpoints import Endpoints
from services.contacts.contact_download_by_id.models.contact_download_by_id_model import (
    ContactDownloadByIdModel,
)
from src.support.helper import Helper


class ContactDownloadByIdAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/contacts/{contact_id}/download")
    def download_contact(self, contact_id: int, *, app_id: str | None = None) -> tuple[requests.Response, ContactDownloadByIdModel]:
        response = self._call(
            "GET",
            url=self.endpoints.download_contact_by_id_endpoint.format(contact_id=int(contact_id)),
            headers=self.build_headers(app_id=app_id, accept="*/*"),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        body_text = response.text
        return response, ContactDownloadByIdModel(
            content_type=response.headers.get("Content-Type") or response.headers.get("content-type") or "",
            body_text=body_text,
            is_vcard="BEGIN:VCARD" in body_text and "END:VCARD" in body_text,
        )
