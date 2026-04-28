import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import CARD_V2_BY_ACCOUNT_PATH, EMPLOYEE_INVITATION_DELETE_PATH
from src.resources.api import get_card_v2_by_account
from src.resources.helpers import parse_card_v2_minimal
from tests.e2e.employee.helpers import wait_for_account_present
from src.support.waiter import wait_until


@allure.epic("LK")
@allure.feature("Employee")
@pytest.mark.employee
@pytest.mark.e2e
class TestEmployeeInvitationEditDeleteFlow:
    @allure.title("Create invitation returns id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_created_employee_returns_id(self, employee_invite_card_flow):
        assert employee_invite_card_flow["invite_id"] > 0
        assert employee_invite_card_flow["account_id"] > 0

    @allure.title("Employee appears in accounts list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_employee_present_in_accounts_list(self, lk_api, employee_invite_card_flow):
        account_id = employee_invite_card_flow["account_id"]
        found = wait_for_account_present(lk_api, account_id, timeout_s=40, step_s=2)
        assert found is not None, f"Employee {account_id} not found in /accounts after create"

    @allure.title("PUT Card/V2 updates fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_put_card_v2_updates_fields(self, lk_api, employee_invite_card_flow):
        account_id = int(employee_invite_card_flow["account_id"])
        card_id = int(employee_invite_card_flow["card_id"])
        path = CARD_V2_BY_ACCOUNT_PATH.format(account_id=account_id, card_id=card_id)

        with allure.step(f"PUT {path}"):
            response = lk_api.put(path, json=employee_invite_card_flow["put_body"])

            if response.status_code == HTTPStatus.BAD_REQUEST and "Employment" in employee_invite_card_flow["put_body"]:
                body = employee_invite_card_flow["put_body"]
                employment = body.get("Employment", {})
                if "CompanyID" in employment:
                    employment.pop("CompanyID", None)
                    employment["CompanyId"] = employee_invite_card_flow["updated"]["company_id"]
                    response = lk_api.put(path, json=body)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"PUT Card/V2 failed: {response.status_code} {response.text}"
        )

    @allure.title("Updated fields visible via GET Card/V2")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_updated_fields_visible_via_card_get(self, lk_api, employee_invite_card_flow):
        account_id = int(employee_invite_card_flow["account_id"])
        card_id = int(employee_invite_card_flow["card_id"])
        expected = employee_invite_card_flow["updated"]

        def _ok():
            response = get_card_v2_by_account(lk_api, account_id=account_id, card_id=card_id)
            if response.status_code != HTTPStatus.OK:
                return None
            got = parse_card_v2_minimal(response.json() if response.text else {})
            if got["lastName"] == expected["last"] and got["selfInfo"] == expected["self"]:
                return True
            return None

        ok = wait_until(_ok, timeout_s=60, step_s=3)
        assert ok, (
            f"Updated fields not visible via GET {CARD_V2_BY_ACCOUNT_PATH.format(account_id=account_id, card_id=card_id)}. "
            f"Expected lastName='{expected['last']}', selfInfo='{expected['self']}'"
        )

    @allure.title("Delete invitation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_05_delete_employee(self, lk_api, employee_invite_card_flow):
        subscription_id = employee_invite_card_flow["subscription_id"]
        invite_id = employee_invite_card_flow["invite_id"]

        path = EMPLOYEE_INVITATION_DELETE_PATH.format(
            sub_id=subscription_id,
            invite_id=invite_id,
        )

        with allure.step(f"DELETE {path}"):
            response = lk_api.delete(path)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete failed: {response.status_code} {response.text}"
        )
        employee_invite_card_flow["deleted"] = True

    @allure.title("After delete flag is set")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_06_after_delete_no_strict_check(self, employee_invite_card_flow):
        assert employee_invite_card_flow["deleted"] is True
