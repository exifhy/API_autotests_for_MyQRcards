from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.onboarding_statuses.endpoints import Endpoints
from services.accounts.onboarding_statuses.models.onboarding_statuses_model import OnboardingStatusModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class OnboardingStatusesAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /onboardingStatuses")
    def get_onboarding_statuses(self) -> tuple[requests.Response, list[OnboardingStatusModel]]:
        response = self._call(
            "GET",
            url=self.endpoints.get_onboarding_statuses_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} {data}"
        models = [OnboardingStatusModel(**item) for item in data if isinstance(item, dict)]
        return response, models

    @allure.step("GET /onboardingStatuses without auth")
    def get_onboarding_statuses_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_onboarding_statuses_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
