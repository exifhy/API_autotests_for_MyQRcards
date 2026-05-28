import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_patch_v2.api_accounts_card_patch_v2 import AccountsCardPatchV2API
from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from testkit.fixtures.employee import _bulk_employee_flow
from tests.e2e.employee.helpers import (
    wait_for_all_first_names_absent_in_company,
    wait_for_all_first_names_present,
)


@allure.epic("LK")
@allure.feature("Employee")
@pytest.mark.e2e
@pytest.mark.employee
@allure.description("/Employee — create 4 via invitation, verify, move to target company, verify, delete flow")
class TestEmployeeInvitationAddMoveInCompanyDeleteFlow:

    @allure.title("POST invitations x4 → list → PATCH move → list in target → DELETE → absent in target")
    @pytest.mark.smoke
    def test_employee_invitation_add_moveincompany_delete_flow(self, lk_api, cfg):
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
                    email_prefix="autotest_move",
                    first_prefix="AT_MoveFN",
                    phone_prefix="8999333",
                    target_company_id=target_company_id,
                )
                created = flow["created"]
                assert len(created) == 4
                for emp in created:
                    assert emp["invite_id"] > 0
                    assert emp["account_id"] > 0
                    assert emp["first_name"]

            with allure.step("02. GET /accounts — verify all 4 employees appear in list"):
                first_names = [emp["first_name"] for emp in created]
                ok = wait_for_all_first_names_present(lk_api, first_names, timeout_s=60, step_s=3)
                assert ok, "Not all 4 created employees found in /accounts list"

            with allure.step(f"03. PATCH /accounts/{{id}}/cards/{{card_id}} x4 — move to target company {target_company_id}"):
                patch_body = [{"Field": "CompanyID", "Value": target_company_id}]
                for emp in created:
                    account_id = emp["account_id"]
                    card_id = int(emp["card_id"])
                    response = AccountsCardPatchV2API().patch_accounts_card_v2(account_id, card_id, patch_body)
                    assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                        f"PATCH move failed for account_id={account_id}: {response.status_code} {response.text}"
                    )

            with allure.step(f"04. GET /accounts?companyID={target_company_id} — verify all 4 visible in target"):
                ok = wait_for_all_first_names_present(
                    lk_api,
                    first_names,
                    company_id=target_company_id,
                    timeout_s=90,
                    step_s=3,
                )
                assert ok, f"Not all 4 employees found in /accounts?companyID={target_company_id}"

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
                ok = wait_for_all_first_names_absent_in_company(
                    lk_api,
                    first_names,
                    company_id=target_company_id,
                    timeout_s=120,
                    step_s=5,
                )
                assert ok, f"Some deleted employees still visible in companyID={target_company_id}"

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
