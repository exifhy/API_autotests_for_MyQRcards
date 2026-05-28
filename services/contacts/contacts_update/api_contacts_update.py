from __future__ import annotations

from http import HTTPStatus

import allure
import requests

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contacts_update.endpoints import Endpoints
from src.support.helper import Helper


class ContactsUpdateAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /accounts/contacts")
    def update_contact(self, payload: dict, *, app_id: str | None = None) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.update_contacts_endpoint,
            headers=self.build_headers(app_id=app_id),
            json=payload,
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        return response
