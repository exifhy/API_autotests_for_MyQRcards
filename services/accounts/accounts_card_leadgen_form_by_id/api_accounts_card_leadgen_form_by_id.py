from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_leadgen_form_by_id.endpoints import Endpoints
from services.cards.card_leadgen_form_by_id.models.card_leadgen_form_by_id_model import (
    CardLeadGenFormByIdModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardLeadGenFormByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/leadGenForms/{leadgen_form_id}")
    def get_accounts_card_leadgen_form_by_id(
        self,
        account_id: int,
        card_id: int,
        leadgen_form_id: int,
    ) -> CardLeadGenFormByIdModel:
        response = None
        for attempt in range(5):
            response = self._call(
                "GET",
                url=self.endpoints.get_accounts_card_leadgen_form_by_id_endpoint.format(
                    account_id=int(account_id),
                    card_id=int(card_id),
                    leadgen_form_id=int(leadgen_form_id),
                ),
                headers=Headers.auth_header(bearer_token=get_token()),
            )
            if response.status_code == HTTPStatus.OK:
                break
            if response.status_code not in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND):
                break
            if attempt < 4:
                time.sleep(2)
        assert response is not None
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert int(data["cardID"]) == int(card_id), f"Expected cardID={card_id}, got {data.get('cardID')}"
        assert int(data["id"]) == int(leadgen_form_id), (
            f"Expected leadGenFormID={leadgen_form_id}, got {data.get('id')}"
        )
        return CardLeadGenFormByIdModel(**data)
