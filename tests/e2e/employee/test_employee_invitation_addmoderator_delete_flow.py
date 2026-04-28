import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_moderator_get.api_subscription_moderator_get import (
    SubscriptionModeratorGetAPI,
)
from services.subscriptions.subscription_moderators_add.api_subscription_moderators_add import (
    SubscriptionModeratorsAddAPI,
)
from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from tests.e2e.employee.helpers import wait_for_account_present
from src.support.waiter import wait_until


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invitation -> Add moderator -> Verify -> Delete")
@pytest.mark.e2e
@pytest.mark.employee
class TestEmployeeInvitationAddModeratorDeleteFlowV1:
    @allure.title("Employee created")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_employee_created(self, employee_invite_card_flow):
        assert employee_invite_card_flow["invite_id"] > 0
        assert employee_invite_card_flow["account_id"] > 0

        allure.attach(
            str(employee_invite_card_flow["invite_id"]),
            "invite_id",
            allure.attachment_type.TEXT,
        )
        allure.attach(
            str(employee_invite_card_flow["account_id"]),
            "account_id",
            allure.attachment_type.TEXT,
        )

        email = (employee_invite_card_flow.get("created") or {}).get("email")
        if email:
            allure.attach(email, "employee_email", allure.attachment_type.TEXT)

    @allure.title("Employee appears in accounts list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_employee_present_in_accounts_list(self, lk_api, employee_invite_card_flow):
        account_id = int(employee_invite_card_flow["account_id"])
        with allure.step(f"Wait employee id={account_id} appears in /accounts"):
            found = wait_for_account_present(lk_api, account_id, timeout_s=60, step_s=3)

        assert found is not None, f"Employee {account_id} not found in /accounts after create"

    @allure.title("Add moderator")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_add_moderator(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        account_id = int(employee_invite_card_flow["account_id"])

        response = SubscriptionModeratorsAddAPI().add_subscription_moderator(sub_id, account_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.CONFLICT), (
            f"Add moderator failed: {response.status_code} {response.text}"
        )

    @allure.title("Moderator visible via GET")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_04_moderator_get_623(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        account_id = int(employee_invite_card_flow["account_id"])

        def _ok():
            data = SubscriptionModeratorGetAPI().get_subscription_moderator(sub_id, account_id)
            payload = data.model_dump()
            return payload if int(payload.get("accountID", -1)) == account_id else None

        with allure.step("Wait moderator visible via 623"):
            data = wait_until(_ok, timeout_s=60, step_s=3)

        assert data is not None, "Moderator not visible via 623"

        allure.attach(
            str(data.get("accountID")),
            "moderator_accountID",
            allure.attachment_type.TEXT,
        )
        allure.attach(
            str(data.get("cardID")),
            "moderator_cardID",
            allure.attachment_type.TEXT,
        )

    @allure.title("Delete invitation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_05_delete_employee(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        invite_id = int(employee_invite_card_flow["invite_id"])

        delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)

        with allure.step(f"DELETE {delete_path}"):
            response = lk_api.delete(delete_path)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete invitation failed: {response.status_code} {response.text}"
        )
        employee_invite_card_flow["deleted"] = True
