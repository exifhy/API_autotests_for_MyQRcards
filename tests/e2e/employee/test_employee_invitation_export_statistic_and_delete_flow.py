from datetime import datetime, timedelta
from http import HTTPStatus

import allure
import pytest

from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH, EXPORTS_STATISTIC_PATH
from tests.e2e.employee.helpers import wait_for_account_present


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invitation -> Export statistic -> Delete (SMOKE)")
@pytest.mark.e2e
@pytest.mark.employee
@allure.description(
    """
    Invitation create -> accounts list verify -> export statistic -> delete.
    """
)
class TestEmployeeInvitationExportStatisticAndDeleteFlow:
    @allure.title("Employee created")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_employee_created(self, employee_stat_export_flow):
        assert employee_stat_export_flow["account_id"] > 0
        assert employee_stat_export_flow["invite_id"] > 0

        allure.attach(
            str(employee_stat_export_flow["invite_id"]),
            "invite_id",
            allure.attachment_type.TEXT,
        )
        allure.attach(
            employee_stat_export_flow["email"],
            "employee_email",
            allure.attachment_type.TEXT,
        )

    @allure.title("Employee appears in accounts list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_employee_present_in_accounts_list(self, lk_api, employee_stat_export_flow):
        account_id = employee_stat_export_flow["account_id"]
        with allure.step(f"Wait employee id={account_id} appears in /accounts"):
            found = wait_for_account_present(lk_api, account_id, timeout_s=60, step_s=3)

        assert found is not None, f"Employee {account_id} not found in /accounts after create"

    @allure.title("Statistic export returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_statistic_export_returns_200(self, lk_api):
        now = datetime.now()
        date_from = (now - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
        date_till = now.replace(hour=23, minute=59, second=59, microsecond=0)

        params = {
            "DateFrom": date_from.strftime("%Y-%m-%dT%H:%M:%S"),
            "DateTill": date_till.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        path = EXPORTS_STATISTIC_PATH.split("?")[0]

        with allure.step(f"GET {path} (DateFrom/DateTill)"):
            allure.attach(params["DateFrom"], "DateFrom", allure.attachment_type.TEXT)
            allure.attach(params["DateTill"], "DateTill", allure.attachment_type.TEXT)

            response = lk_api.get(path, params=params)

            allure.attach(str(response.status_code), "export_status", allure.attachment_type.TEXT)
            allure.attach(getattr(response, "url", ""), "export_url", allure.attachment_type.TEXT)
            if response.status_code != HTTPStatus.OK:
                allure.attach(
                    response.text or "",
                    "export_response_text",
                    allure.attachment_type.TEXT,
                )

        assert response.status_code == HTTPStatus.OK, (
            f"Statistic export failed: {response.status_code}, url={getattr(response, 'url', '')}"
        )

    @allure.title("Delete invitation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_04_delete_employee(self, lk_api, employee_stat_export_flow):
        sub_id = employee_stat_export_flow["subscription_id"]
        invite_id = employee_stat_export_flow["invite_id"]
        delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)

        with allure.step(f"DELETE {delete_path}"):
            response = lk_api.delete(delete_path)
            allure.attach(str(response.status_code), "delete_status", allure.attachment_type.TEXT)
            allure.attach(
                response.text or "",
                "delete_response_text",
                allure.attachment_type.TEXT,
            )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete failed: {response.status_code} {response.text}"
        )
        employee_stat_export_flow["deleted"] = True
