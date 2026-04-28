import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from src.resources.api import hide_cards
from tests.e2e.employee.helpers import (
    wait_for_all_account_ids_present,
    wait_for_account_hidden_state,
)


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invitation -> Hide -> Delete")
@pytest.mark.e2e
@pytest.mark.employee
class TestEmployeeInvitationAddHideDeleteFlow:
    @allure.title("Created 3 employees")
    def test_01_created_3_employees(self, employee_hide_flow):
        assert len(employee_hide_flow["created"]) == 3
        assert all(int(item["account_id"]) > 0 for item in employee_hide_flow["created"])

    @allure.title("Employees appear in accounts list")
    def test_02_employees_present_in_accounts_list(self, lk_api, employee_hide_flow):
        ids = {emp["account_id"] for emp in employee_hide_flow["created"]}
        ok = wait_for_all_account_ids_present(lk_api, ids, timeout_s=90, step_s=3)
        assert ok, "Not all created employees were found in /accounts"

    @allure.title("Hide cards for employees")
    def test_03_hide_cards_for_3_employees(self, lk_api, employee_hide_flow):
        body = [{"AccountID": emp["account_id"], "CardID": 1} for emp in employee_hide_flow["created"]]
        response = hide_cards(lk_api, body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Hide failed: {response.status_code} {response.text}"
        )

    @allure.title("Employees become hidden in accounts list")
    def test_04_hidden_flag_true_in_accounts_list(self, lk_api, employee_hide_flow):
        for emp in employee_hide_flow["created"]:
            account_id = emp["account_id"]
            ok = wait_for_account_hidden_state(lk_api, account_id, is_hidden=True, timeout_s=120, step_s=5)
            assert ok, f"Employee {account_id} does not have isHidden=true in /accounts"

    @allure.title("Delete all created employees")
    def test_05_delete_all_created_employees(self, lk_api, employee_hide_flow):
        sub_id = employee_hide_flow["subscription_id"]

        for emp in employee_hide_flow["created"]:
            invite_id = emp["invite_id"]
            delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)
            response = lk_api.delete(delete_path)
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                f"Delete failed for {invite_id}: {response.status_code} {response.text}"
            )
            employee_hide_flow["deleted_ids"].add(invite_id)
