from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_virtualbackgrounds.endpoints import Endpoints
from services.virtual_backgrounds.virtual_backgrounds_list.models.virtual_backgrounds_model import (
    VirtualBackgroundItemModel,
    VirtualBackgroundsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardVirtualBackgroundsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/virtualbackground")
    def get_accounts_card_virtualbackgrounds(self, account_id: int, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.accounts_card_virtualbackgrounds_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [VirtualBackgroundItemModel(**item) for item in data if isinstance(item, dict)]
        return response, VirtualBackgroundsModel(items=items)
