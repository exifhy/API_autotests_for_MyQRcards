from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_custom_message_template_by_id.endpoints import Endpoints
from services.accounts.accounts_custom_message_templates.models.accounts_custom_message_templates_model import (
    AccountCustomMessageTemplateModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCustomMessageTemplateByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/CustomMessageTemplates/{template_id}")
    def get_accounts_custom_message_template_by_id(self, account_id: int, template_id: int):
        last_error = None
        response = None
        for attempt in range(2):
            try:
                response = self._call(
                    "GET",
                    url=self.endpoints.get_accounts_custom_message_template_by_id_endpoint.format(
                        account_id=int(account_id),
                        template_id=int(template_id),
                    ),
                    headers=Headers.auth_header(bearer_token=get_token()),
                )
                break
            except requests.RequestException as error:
                last_error = error
                if attempt == 1:
                    raise
                time.sleep(1)

        if response is None:
            raise last_error or RuntimeError("Failed to get custom message template by id")
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        model = AccountCustomMessageTemplateModel(**data)
        assert model.id == template_id, f"Expected template_id={template_id}, got {model.id}"
        return model
