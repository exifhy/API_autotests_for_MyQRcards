from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_custom_message_template_by_leadgen_form.endpoints import Endpoints
from services.accounts.accounts_custom_message_templates.models.accounts_custom_message_templates_model import (
    AccountCustomMessageTemplateModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCustomMessageTemplateByLeadGenFormAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/LeadGenForms/{leadgen_form_id}/MessageTemplate")
    def get_accounts_custom_message_template_by_leadgen_form(
        self,
        account_id: int,
        card_id: int,
        leadgen_form_id: int,
    ) -> AccountCustomMessageTemplateModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_custom_message_template_by_leadgen_form_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                leadgen_form_id=int(leadgen_form_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return AccountCustomMessageTemplateModel(**data)

