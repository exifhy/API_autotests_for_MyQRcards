from http import HTTPStatus

import allure
import requests

from services.accounts.accounts_contact_create_for_owner.endpoints import Endpoints
from services.contacts.base_api import ContactsBaseAPI
from services.contacts.contact_create_app.models.contact_create_app_model import (
    ContactCreateAppModel,
)
from src.support.helper import Helper


class AccountsContactCreateForOwnerAPI(Helper, ContactsBaseAPI):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/{account_id}/Contacts")
    def create_contact_for_owner(
        self,
        account_id: int,
        payload: dict,
        *,
        app_id: str | None = None,
    ) -> tuple[requests.Response, ContactCreateAppModel]:
        response = self._call(
            "POST",
            url=self.endpoints.create_contact_for_owner_endpoint.format(account_id=int(account_id)),
            headers=self.build_headers(app_id=app_id),
            json=payload,
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return response, ContactCreateAppModel(**response.json())
