import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_moderators_add.api_subscription_moderators_add import (
    SubscriptionModeratorsAddAPI,
)
from services.subscriptions.subscription_moderators_delete.api_subscription_moderators_delete import (
    SubscriptionModeratorsDeleteAPI,
)
from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from tests.e2e.employee.helpers import (
    wait_for_account_present,
    wait_for_moderator_absent,
    wait_for_moderator_present,
)


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invitation -> Add moderator -> Delete moderator -> Delete employee")
@pytest.mark.e2e
@pytest.mark.employee
class TestEmployeeInvitationAddAndDeleteModeratorDeleteFlow:
    @allure.title("Employee created")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_employee_created(self, employee_invite_card_flow):
        assert employee_invite_card_flow["invite_id"] > 0
        assert employee_invite_card_flow["account_id"] > 0

    @allure.title("Employee appears in accounts list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_employee_present_in_accounts_list(self, lk_api, employee_invite_card_flow):
        account_id = int(employee_invite_card_flow["account_id"])
        found = wait_for_account_present(lk_api, account_id, timeout_s=60, step_s=3)
        assert found is not None, f"Employee {account_id} not found in /accounts"

    @allure.title("Add moderator")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_add_moderator(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        account_id = int(employee_invite_card_flow["account_id"])

        response = SubscriptionModeratorsAddAPI().add_subscription_moderator(sub_id, account_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.CONFLICT), (
            f"Add moderator failed: {response.status_code} {response.text}"
        )

    @allure.title("Moderator appears in moderators list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_moderator_present_in_list(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        account_id = int(employee_invite_card_flow["account_id"])
        found = wait_for_moderator_present(
            lk_api,
            sub_id=sub_id,
            account_id=account_id,
            timeout_s=120,
            step_s=5,
        )
        assert found is not None, f"Moderator {account_id} not found in moderators list"

    @allure.title("Delete moderator")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_05_delete_moderator(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        account_id = int(employee_invite_card_flow["account_id"])

        response = SubscriptionModeratorsDeleteAPI().delete_subscription_moderator(sub_id, account_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT), (
            f"Delete moderator failed: {response.status_code} {response.text}"
        )

    @allure.title("Moderator disappears from moderators list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_06_moderator_absent_in_list(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        account_id = int(employee_invite_card_flow["account_id"])
        ok = wait_for_moderator_absent(
            lk_api,
            sub_id=sub_id,
            account_id=account_id,
            timeout_s=120,
            step_s=5,
        )
        assert ok, f"Moderator {account_id} is still present in moderators list"

    @allure.title("Delete invitation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_07_delete_employee(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        invite_id = int(employee_invite_card_flow["invite_id"])
        delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)

        response = lk_api.delete(delete_path)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND), (
            f"Delete invitation failed: {response.status_code} {response.text}"
        )
        employee_invite_card_flow["deleted"] = True
