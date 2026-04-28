import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from src.resources.api import accounts_list, hide_cards, show_cards
from tests.e2e.employee.helpers import wait_for_account_hidden_state, wait_for_account_present


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invitation -> Hide -> Show -> Delete")
@pytest.mark.e2e
@pytest.mark.employee
class TestEmployeeInvitationAddHideShowDeleteFlow:
    @allure.title("Created 3 employees")
    def test_01_created_three_employees(self, employee_hide_show_flow):
        assert len(employee_hide_show_flow["created"]) == 3
        assert all(int(emp["account_id"]) > 0 for emp in employee_hide_show_flow["created"])

    @allure.title("Employees present in accounts list")
    def test_02_employees_present_in_accounts_list(self, lk_api, employee_hide_show_flow):
        for emp in employee_hide_show_flow["created"]:
            account_id = emp["account_id"]
            found = wait_for_account_present(lk_api, account_id, timeout_s=60, step_s=3)
            assert found is not None, f"Employee {account_id} not found in /accounts"

    @allure.title("Hide employees")
    def test_03_hide_employees(self, lk_api, employee_hide_show_flow):
        body = [{"AccountID": emp["account_id"], "CardID": 1} for emp in employee_hide_show_flow["created"]]
        response = hide_cards(lk_api, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Hide failed: {response.status_code} {response.text}"
        )

    @allure.title("Employees hidden in accounts list")
    def test_04_employees_hidden_in_accounts_list(self, lk_api, employee_hide_show_flow):
        for emp in employee_hide_show_flow["created"]:
            account_id = emp["account_id"]
            ok = wait_for_account_hidden_state(lk_api, account_id, is_hidden=True, timeout_s=90, step_s=5)
            assert ok, f"Employee {account_id} not hidden (isHidden!=true)"

    @allure.title("Show employees")
    def test_05_show_employees(self, lk_api, employee_hide_show_flow):
        body = [{"AccountID": emp["account_id"], "CardID": 1} for emp in employee_hide_show_flow["created"]]
        response = show_cards(lk_api, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Show failed: {response.status_code} {response.text}"
        )

    @allure.title("Employees visible in accounts list")
    def test_06_employees_visible_in_accounts_list(self, lk_api, employee_hide_show_flow):
        for emp in employee_hide_show_flow["created"]:
            account_id = emp["account_id"]
            ok = wait_for_account_hidden_state(lk_api, account_id, is_hidden=False, timeout_s=90, step_s=5)
            assert ok, f"Employee {account_id} not visible (isHidden!=false)"

    @allure.title("Delete employees")
    def test_07_delete_employees(self, lk_api, employee_hide_show_flow):
        sub_id = employee_hide_show_flow["subscription_id"]
        for emp in employee_hide_show_flow["created"]:
            invite_id = emp["invite_id"]
            delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)
            response = lk_api.delete(delete_path)
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                f"Delete failed for {invite_id}: {response.status_code} {response.text}"
            )
            employee_hide_show_flow["deleted_ids"].add(invite_id)
