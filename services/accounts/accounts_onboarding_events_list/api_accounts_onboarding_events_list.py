from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_onboarding_events_list.endpoints import Endpoints
from services.accounts.accounts_onboarding_events_list.models.account_onboarding_event_model import (
    AccountOnboardingEventModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsOnboardingEventsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/onboardingEvents")
    def get_onboarding_events(self) -> list[AccountOnboardingEventModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_account_onboarding_events_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        return [AccountOnboardingEventModel(**item) for item in response.json()]

    @allure.step("GET /Accounts/onboardingEvents (without auth)")
    def get_onboarding_events_without_auth(self):
        return self._call(
            "GET",
            url=self.endpoints.get_account_onboarding_events_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
