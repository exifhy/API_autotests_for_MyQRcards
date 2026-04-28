from __future__ import annotations

from http import HTTPStatus

import allure

from services.contacts.contact_create_web.endpoints import Endpoints
from services.contacts.contact_create_web.models.contact_create_web_model import (
    ContactCreateWebModel,
)
from src.support.helper import Helper


class ContactCreateWebAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accounts/contacts/web")
    def create_contact(self, payload: dict):
        response = self._call(
            "POST",
            url=self.endpoints.create_contact_web_endpoint,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.CREATED/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"

        data = response.json() if response.text else {}
        if not isinstance(data, dict):
            data = {}
        return response, ContactCreateWebModel(id=data.get("id"))
