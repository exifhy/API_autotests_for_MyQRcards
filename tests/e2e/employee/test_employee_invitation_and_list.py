import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import EMPLOYEE_INVITATION_CREATE_PATH, EMPLOYEE_INVITATION_DELETE_PATH
from src.utils.randoms import rand_email, rand_word


@allure.epic("LK")
@allure.feature("Employee")
@allure.title("Invite employee and find in accounts list")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.employee
@pytest.mark.accounts
def test_invite_employee_and_find_in_accounts_list(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    company_id_create = int(cfg["company_id_create"])

    payload = {
        "Email": rand_email(domain="mail.com"),
        "FirstName": rand_word("AT_Nikita", 6),
        "LastName": rand_word("AT_Test", 6),
        "CompanyID": company_id_create,
        "Phone": "+79" + rand_word("", 9).replace("_", "")[:9],
        "Position": "Director",
        "IsAcceptAdvertising": False,
    }

    employee_id = None
    create_path = EMPLOYEE_INVITATION_CREATE_PATH.format(sub_id=subscription_id)

    with allure.step(f"Create invitation: POST {create_path}"):
        allure.attach(
            str(payload),
            name="request_body",
            attachment_type=allure.attachment_type.JSON,
        )

        response = lk_api.post(create_path, json=payload)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Unexpected status for invitation: {response.status_code}, body={response.text}"
        )

        data = response.json() if response.text else {}
        employee_id = int(data.get("id", 0))
        assert employee_id > 0, f"Response has no valid 'id': {data}"

        allure.attach(
            str(employee_id),
            name="employee_id",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            payload["Email"],
            name="employee_email",
            attachment_type=allure.attachment_type.TEXT,
        )

    try:
        with allure.step("Accounts list: GET /accounts"):
            response = lk_api.get("/accounts?IsIncludeSubscriptionOwner=true")
            assert response.status_code == HTTPStatus.OK, (
                f"Accounts list status: {response.status_code}, body={response.text}"
            )

            accounts = response.json()
            assert isinstance(accounts, list), (
                f"Accounts response is not list: {type(accounts)}"
            )

            allure.attach(
                str(accounts[:20]),
                name="accounts_list_preview",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Check employee_id exists in accounts list"):
            ids = {
                int(account.get("id"))
                for account in accounts
                if isinstance(account, dict) and account.get("id")
            }
            assert employee_id in ids, f"Employee {employee_id} not found in accounts list"

    finally:
        if employee_id:
            delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(
                sub_id=subscription_id,
                invite_id=employee_id,
            )
            with allure.step(f"Cleanup: DELETE {delete_path}"):
                lk_api.delete(delete_path)
