import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from src.resources.api import copy_cards_to_company
from testkit.fixtures.employee import _bulk_employee_flow
from tests.e2e.employee.helpers import (
    wait_for_all_account_ids_absent_in_company,
    wait_for_all_account_ids_present,
    wait_for_all_account_ids_present_in_company,
)


@allure.epic("LK")
@allure.feature("Employee")
@pytest.mark.e2e
@pytest.mark.employee
@allure.description("/Employee — create 4 via invitation, verify, copy cards to target company, verify, delete flow")
class TestEmployeeInvitationAddCopyInCompanyDeleteFlow:

    @allure.title("POST invitations x4 → list → copy cards → list in target → DELETE → absent in target")
    @pytest.mark.smoke
    def test_employee_invitation_add_copyincompany_delete_flow(self, lk_api, cfg):
        subscription_id = int(cfg["subscription_id"])
        source_company_id = int(cfg["company_id_create"])
        target_company_id = int(cfg["company_id_target"])
        created = []
        deleted_invite_ids: set[int] = set()
        try:
            with allure.step("01. POST /Subscriptions/{sub_id}/invitation x4 — create 4 employees"):
                flow = _bulk_employee_flow(
                    lk_api,
                    subscription_id=subscription_id,
                    company_id=source_company_id,
                    count=4,
                    email_prefix="autotest_copy",
                    first_prefix="AT_CopyFN",
                    phone_prefix="8999222",
                    target_company_id=target_company_id,
                )
                created = flow["created"]
                assert len(created) == 4
                assert all(emp["invite_id"] > 0 for emp in created)

            with allure.step("02. GET /accounts — verify all 4 employees appear in list"):
                account_ids = {emp["account_id"] for emp in created}
                ok = wait_for_all_account_ids_present(lk_api, account_ids, timeout_s=60, step_s=3)
                assert ok, f"Not all created employees are visible in /accounts. expected={sorted(account_ids)}"

            with allure.step(f"03. POST copy cards — copy all 4 cards to target company {target_company_id}"):
                body = [
                    {"AccountID": emp["account_id"], "CardID": 1, "CompanyID": target_company_id}
                    for emp in created
                ]
                response = copy_cards_to_company(lk_api, body)
                assert response.status_code in (
                    HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT
                ), f"Card copy failed: {response.status_code} {response.text}"

            with allure.step(f"04. GET /accounts?companyID={target_company_id} — verify all 4 visible in target"):
                ok = wait_for_all_account_ids_present_in_company(
                    lk_api,
                    account_ids,
                    company_id=target_company_id,
                    timeout_s=90,
                    step_s=5,
                )
                assert ok, f"Employees not visible in target companyID={target_company_id}"

            with allure.step("05. DELETE /Subscriptions/{sub_id}/invitation/{invite_id} x4 — delete all employees"):
                for emp in created:
                    invite_id = emp["invite_id"]
                    delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(
                        sub_id=subscription_id, invite_id=invite_id
                    )
                    response = lk_api.delete(delete_path)
                    assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                        f"Delete failed for invite_id={invite_id}: {response.status_code} {response.text}"
                    )
                    deleted_invite_ids.add(invite_id)

            with allure.step(f"06. GET /accounts?companyID={target_company_id} — verify all 4 absent after delete"):
                ok = wait_for_all_account_ids_absent_in_company(
                    lk_api,
                    account_ids,
                    company_id=target_company_id,
                    timeout_s=120,
                    step_s=5,
                )
                assert ok, f"After delete, employees still visible in target companyID={target_company_id}"

        finally:
            for emp in created:
                invite_id = emp["invite_id"]
                if invite_id not in deleted_invite_ids:
                    try:
                        delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(
                            sub_id=subscription_id, invite_id=invite_id
                        )
                        lk_api.delete(delete_path)
                    except Exception:
                        pass
