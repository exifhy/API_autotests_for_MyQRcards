from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_contact_by_id.endpoints import Endpoints
from services.accounts.accounts_contact_by_id.models.accounts_contact_by_id_model import AccountContactByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsContactByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/contacts/{contact_id}")
    def get_contact_by_id(self, contact_id: int) -> AccountContactByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_contact_by_id_endpoint.format(contact_id=contact_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict json, got {type(data)}"
        assert "contactID" in data, "contactID missing"
        assert int(data["contactID"]) == int(contact_id), "contactID mismatch"
        return AccountContactByIdModel(**data)
