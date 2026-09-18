from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_onboarding_event_add.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsOnboardingEventAddAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/onboardingEvents/{type_id}")
    def add_onboarding_event(self, type_id: int):
        response = self._call(
            "POST",
            url=self.endpoints.add_account_onboarding_event_endpoint.format(type_id=type_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected 202, got {response.status_code}: {response.text}"
        )
        return response

    @allure.step("POST /Accounts/onboardingEvents/{type_id} (raw, no assert — for negative cases)")
    def add_onboarding_event_raw(self, type_id):
        return self._call(
            "POST",
            url=self.endpoints.add_account_onboarding_event_endpoint.format(type_id=type_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )

    @allure.step("POST /Accounts/onboardingEvents/{type_id} (without auth)")
    def add_onboarding_event_without_auth(self, type_id: int):
        return self._call(
            "POST",
            url=self.endpoints.add_account_onboarding_event_endpoint.format(type_id=type_id),
            headers=Headers.without_authorization_field_header(),
        )
