from __future__ import annotations

from http import HTTPStatus

import allure

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contact_by_id.endpoints import Endpoints
from services.contacts.contact_by_id.models.contact_by_id_model import ContactByIdModel
from src.support.helper import Helper


class ContactByIdAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/contacts/{contact_id}")
    def get_contact(self, contact_id: int, *, app_id: str | None = None) -> ContactByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_contact_by_id_endpoint.format(contact_id=int(contact_id)),
            headers=self.build_headers(app_id=app_id),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return ContactByIdModel(**response.json())
