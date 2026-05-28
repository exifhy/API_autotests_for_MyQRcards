from __future__ import annotations

from http import HTTPStatus

import allure

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contact_create_app.endpoints import Endpoints
from services.contacts.contact_create_app.models.contact_create_app_model import (
    ContactCreateAppModel,
)
from src.support.helper import Helper


class ContactCreateAppAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accounts/contacts/app")
    def create_contact(self, payload: dict, *, app_id: str | None = None) -> ContactCreateAppModel:
        response = self._call(
            "POST",
            url=self.endpoints.create_contact_app_endpoint,
            headers=self.build_headers(app_id=app_id),
            json=payload,
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return ContactCreateAppModel(**response.json())
