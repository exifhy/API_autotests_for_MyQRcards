from http import HTTPStatus

import allure
import pytest

from services.manager.manager_daily_limit.api_manager_daily_limit import ManagerDailyLimitAPI


@allure.epic("API")
@allure.feature("Manager")
@pytest.mark.api
@allure.description(
    """
    GET /Manager/dailylimit
    REQUIREMENT 29760 — админка для сейлов.
    Позитивный сценарий — под менеджерским аккаунтом (TEST_LK_JWT / get_manager_jwt()).
    """
)
class TestManagerDailyLimit:
    @allure.title("GET /Manager/dailylimit — менеджерский аккаунт получает лимит")
    @pytest.mark.smoke
    def test_manager_daily_limit_flow(self):
        model = ManagerDailyLimitAPI().get_manager_daily_limit()
        assert model.dailyLimit > 0, f"Expected positive dailyLimit, got {model.dailyLimit}"
        assert model.usedToday >= 0, f"Expected non-negative usedToday, got {model.usedToday}"
        assert model.usedToday <= model.dailyLimit, (
            f"usedToday ({model.usedToday}) exceeds dailyLimit ({model.dailyLimit})"
        )

    @allure.title("GET /Manager/dailylimit — обычный (не-менеджерский) аккаунт получает отказ")
    @pytest.mark.smoke
    def test_manager_daily_limit_non_manager_account(self):
        response = ManagerDailyLimitAPI().get_manager_daily_limit_raw()
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected 409 (code=NotFound, 'Manager не найден') for non-manager account, "
            f"got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data[0]["code"] == "NotFound", f"Expected code=NotFound, got: {data}"

    @allure.title("GET /Manager/dailylimit без авторизации")
    @pytest.mark.smoke
    def test_manager_daily_limit_without_auth(self):
        response = ManagerDailyLimitAPI().get_manager_daily_limit_without_auth()
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f"Expected 401, got {response.status_code}: {response.text}"
        )
