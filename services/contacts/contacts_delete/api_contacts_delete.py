from __future__ import annotations

from http import HTTPStatus

import allure
import requests

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contacts_delete.endpoints import Endpoints
from src.support.helper import Helper


class ContactsDeleteAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /accounts/contacts")
    def delete_contacts(self, contact_ids: list[int], *, app_id: str | None = None) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_contacts_endpoint,
            headers=self.build_headers(app_id=app_id),
            json=[int(contact_id) for contact_id in contact_ids],
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        return response
