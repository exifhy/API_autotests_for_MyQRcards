import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import ACCOUNTS_LIST_PATH, EMPLOYEE_INVITATION_DELETE_PATH
from tests.e2e.employee.helpers import extract_emails, extract_ids


@allure.epic("LK")
@allure.feature("Employee")
@pytest.mark.e2e
@pytest.mark.employee
@allure.description(
    """
    Invitation create -> accounts list verify -> delete -> accounts list verify.
    """
)
class TestEmployeeInvitationFlow:
    @allure.title("Create invitation returns id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_create_employee_returns_id(self, created_employee, employee_flow_ctx):
        with allure.step("Save invite_id into flow"):
            employee_flow_ctx["invite_id"] = int(created_employee)

        with allure.step("Check invite_id is int and > 0"):
            assert isinstance(employee_flow_ctx["invite_id"], int)
            assert employee_flow_ctx["invite_id"] > 0

    @allure.title("Employee appears in accounts list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_employee_present_in_list(self, lk_api, employee_flow_ctx):
        email = employee_flow_ctx.get("email")
        assert email, "email is empty (test_01 failed?)"

        with allure.step(f"GET {ACCOUNTS_LIST_PATH}"):
            response = lk_api.get(ACCOUNTS_LIST_PATH)
            assert response.status_code == HTTPStatus.OK, (
                f"Accounts list failed ({response.status_code}): {response.text}"
            )

        with allure.step("Extract emails and check created employee is present"):
            emails = extract_emails(response.json())
            assert email.lower() in emails, (
                f"Created employee email={email} not found in accounts list"
            )

    @allure.title("Delete invitation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_delete_employee(self, lk_api, cfg, employee_flow_ctx):
        invite_id = employee_flow_ctx.get("invite_id")
        assert invite_id, "invite_id is empty (test_01 failed?)"

        sub_id = cfg["subscription_id"]
        delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)

        with allure.step(f"DELETE {delete_path}"):
            response = lk_api.delete(delete_path)
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                f"Delete failed ({response.status_code}): {response.text}"
            )

        employee_flow_ctx["deleted"] = True

    @allure.title("Employee disappears from accounts list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_employee_not_in_list_after_delete(self, lk_api, employee_flow_ctx):
        invite_id = employee_flow_ctx.get("invite_id")
        assert invite_id, "invite_id is empty (test_01 failed?)"

        with allure.step(f"GET {ACCOUNTS_LIST_PATH}"):
            response = lk_api.get(ACCOUNTS_LIST_PATH)
            assert response.status_code == HTTPStatus.OK, (
                f"Accounts list failed ({response.status_code}): {response.text}"
            )

        with allure.step("Extract ids and check employee is absent"):
            ids = extract_ids(response.json())
            assert invite_id not in ids, f"Employee id={invite_id} still present after delete"
