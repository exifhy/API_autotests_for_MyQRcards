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
    Позитивный сценарий (валидный менеджер + managerPassword) требует отдельного
    менеджерского аккаунта — пока недоступен, тест не написан.
    """
)
class TestManagerDailyLimit:
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
