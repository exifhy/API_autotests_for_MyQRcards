import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import EMPLOYEE_INVITATION_DELETE_PATH
from src.assertions.social_asserts import (
    build_social_attrs_payload,
    extract_social_names_from_v2,
    has_socials_in_0852,
)
from src.constants.attributes import TELEGRAM_ATTRIBUTE_ID, WHATSAPP_ATTRIBUTE_ID
from src.resources.api import (
    get_card_v2_by_account,
    list_card_attributes_0852,
    merge_card_attributes,
)
from tests.e2e.employee.helpers import wait_for_account_present
from src.support.waiter import wait_until


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invitation -> Add attributes -> Verify -> Delete")
@pytest.mark.e2e
@pytest.mark.employee
class TestEmployeeInvitationAddAttributeDeleteFlow:
    @allure.title("01. Employee created — account_id present")
    def test_01_employee_created(self, employee_invite_card_flow):
        assert employee_invite_card_flow["account_id"] > 0
        allure.attach(
            str(employee_invite_card_flow["account_id"]),
            "account_id",
            allure.attachment_type.TEXT,
        )

    @allure.title("02. Employee appears in /accounts list")
    def test_02_employee_present_in_accounts_list(self, lk_api, employee_invite_card_flow):
        account_id = employee_invite_card_flow["account_id"]
        with allure.step(f"Wait employee id={account_id} appears in /accounts"):
            found = wait_for_account_present(lk_api, account_id, timeout_s=60, step_s=3)

        assert found is not None, "Employee not found in accounts list"

    @allure.title("03. PUT merge social attributes (Telegram + WhatsApp) to card")
    def test_03_add_attributes_to_card(self, lk_api, employee_invite_card_flow):
        account_id = employee_invite_card_flow["account_id"]
        card_id = int(employee_invite_card_flow["card_id"])

        body = build_social_attrs_payload(
            telegram_id=TELEGRAM_ATTRIBUTE_ID,
            whatsapp_id=WHATSAPP_ATTRIBUTE_ID,
            telegram_url="https://t.me/username",
            whatsapp_url="https://wa.me/+79533453434",
        )

        with allure.step(f"PUT merge attributes for account={account_id}, card={card_id}"):
            response = merge_card_attributes(
                lk_api,
                account_id=account_id,
                card_id=card_id,
                body=body,
            )
            allure.attach(str(response.status_code), "merge_status", allure.attachment_type.TEXT)
            if response.status_code not in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT):
                allure.attach(response.text or "", "merge_response_text", allure.attachment_type.TEXT)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Add attributes failed: {response.status_code} {response.text}"
        )

    @allure.title("04. Social attributes visible via V2 / 085.2")
    def test_04_attributes_visible(self, lk_api, employee_invite_card_flow):
        account_id = employee_invite_card_flow["account_id"]
        card_id = int(employee_invite_card_flow["card_id"])
        expected = {"telegram", "whatsapp"}

        def _ok():
            response = get_card_v2_by_account(lk_api, account_id=account_id, card_id=card_id)
            if response is not None and response.status_code == HTTPStatus.OK:
                names = extract_social_names_from_v2(response.json())
                if expected.issubset(names):
                    return True

            fallback = list_card_attributes_0852(lk_api, account_id=account_id, card_id=card_id)
            if fallback.status_code != HTTPStatus.OK:
                return None
            data = fallback.json()
            if not isinstance(data, list):
                return None
            return True if has_socials_in_0852(data, expected) else None

        with allure.step("Wait attributes appear in V2 or 085.2"):
            ok = wait_until(_ok, timeout_s=90, step_s=5)

        assert ok, "Attributes not visible via V2/085.2"

    @allure.title("05. DELETE employee invitation")
    def test_05_delete_employee(self, lk_api, employee_invite_card_flow):
        sub_id = int(employee_invite_card_flow["subscription_id"])
        invite_id = int(employee_invite_card_flow["invite_id"])

        path = EMPLOYEE_INVITATION_DELETE_PATH.format(sub_id=sub_id, invite_id=invite_id)

        with allure.step(f"DELETE {path}"):
            response = lk_api.delete(path)
            allure.attach(str(response.status_code), "delete_status", allure.attachment_type.TEXT)
            if response.status_code not in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT):
                allure.attach(response.text or "", "delete_response_text", allure.attachment_type.TEXT)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete failed: {response.status_code} {response.text}"
        )
        employee_invite_card_flow["deleted"] = True
