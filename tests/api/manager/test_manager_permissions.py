from http import HTTPStatus

import allure
import pytest

from services.manager.manager_permissions.api_manager_permissions import ManagerPermissionsAPI


@allure.epic("API")
@allure.feature("Manager")
@pytest.mark.api
@allure.description(
    """
    GET /Manager/permissions
    REQUIREMENT 29760 — админка для сейлов.
    Позитивный сценарий — под менеджерским аккаунтом (TEST_LK_JWT / get_manager_jwt()).
    """
)
class TestManagerPermissions:
    @allure.title("GET /Manager/permissions — менеджерский аккаунт получает список прав")
    @pytest.mark.smoke
    def test_manager_permissions_flow(self):
        model = ManagerPermissionsAPI().get_manager_permissions()
        assert model.items, "Expected non-empty permissions list"
        names = {item.name for item in model.items}
        assert "CreateSubscription" in names, f"Expected CreateSubscription in permissions, got: {names}"

    @allure.title("GET /Manager/permissions — обычный (не-менеджерский) аккаунт получает отказ")
    @pytest.mark.smoke
    def test_manager_permissions_non_manager_account(self):
        response = ManagerPermissionsAPI().get_manager_permissions_raw()
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected 409 (code=NotFound, 'Manager не найден') for non-manager account, "
            f"got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data[0]["code"] == "NotFound", f"Expected code=NotFound, got: {data}"

    @allure.title("GET /Manager/permissions без авторизации")
    @pytest.mark.smoke
    def test_manager_permissions_without_auth(self):
        response = ManagerPermissionsAPI().get_manager_permissions_without_auth()
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f"Expected 401, got {response.status_code}: {response.text}"
        )
