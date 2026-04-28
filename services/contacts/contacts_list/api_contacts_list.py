from __future__ import annotations

from http import HTTPStatus

import allure
import requests

from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contacts_list.endpoints import Endpoints
from services.contacts.contacts_list.models.contacts_list_model import ContactListItemModel
from src.support.helper import Helper


class ContactsListAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/contacts")
    def get_contacts(
        self,
        *,
        params: dict | None = None,
        app_id: str | None = None,
    ) -> tuple[requests.Response, list[ContactListItemModel]]:
        response = self._call(
            "GET",
            url=self.endpoints.get_contacts_endpoint,
            headers=self.build_headers(app_id=app_id),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.PARTIAL_CONTENT, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        return response, [ContactListItemModel(**item) for item in data]
