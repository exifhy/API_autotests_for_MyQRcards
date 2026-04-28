import allure
import pytest
from http import HTTPStatus

from services.accounts.onboarding_statuses.api_onboarding_statuses import OnboardingStatusesAPI


@allure.epic("API")
@allure.feature("Accounts")
@allure.title("Onboarding statuses")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /onboardingStatuses
    """
)
class TestOnboardingStatuses:
    @allure.title("GET /onboardingStatuses → 200, non-empty list with id and nameRu")
    @pytest.mark.smoke
    def test_get_onboarding_statuses_200(self):
        response, items = OnboardingStatusesAPI().get_onboarding_statuses()

        assert response.status_code == HTTPStatus.OK
        assert isinstance(items, list)
        assert len(items) > 0, "Expected non-empty statuses list"
        assert all(item.id for item in items)
        assert all(item.nameRu for item in items)

    @allure.title("GET /onboardingStatuses without auth → 401/403")
    @pytest.mark.ng
    def test_get_onboarding_statuses_401_without_auth(self):
        response = OnboardingStatusesAPI().get_onboarding_statuses_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
