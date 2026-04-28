import time
from http import HTTPStatus

import allure
import pytest

from services.accounts.accounts_contact_create_for_owner.api_accounts_contact_create_for_owner import (
    AccountsContactCreateForOwnerAPI,
)
from services.contacts.contact_by_id.api_contact_by_id import ContactByIdAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    POST /Accounts/{accountID}/Contacts
    GET /accounts/contacts/{contact_id}
    DELETE /subscriptions/{sub_id}/contacts
    """
)
class TestAccountsContactCreateForOwner:
    @allure.title("POST /Accounts/{accountID}/Contacts creates contact visible by GET and removable by DELETE")
    def test_accounts_contact_create_for_owner_flow(self, cfg):
        now = int(time.time())
        app_id = str(cfg.get("x_application_id") or "3")
        payload = {
            "FirstName": f"Owner_{now}",
            "LastName": f"Contact_{now}",
            "Email": f"owner_contact_{now}@tt.tt",
            "MobilePhone": f"+79{now % 1000000000:09d}",
            "Position": f"Tester_{now}",
            "CompanyName": f"Company_{now}",
            "Description": f"Desc_{now}",
        }

        contact_id = None
        try:
            with allure.step("POST /Accounts/{accountID}/Contacts — create contact"):
                response, created = AccountsContactCreateForOwnerAPI().create_contact_for_owner(
                    int(cfg["lk_account_id"]),
                    payload,
                    app_id=app_id,
                )
                assert response.status_code == HTTPStatus.CREATED
                assert created.id is not None
                contact_id = int(created.id)

            with allure.step(f"GET /accounts/contacts/{contact_id} — verify fields"):
                fetched = ContactByIdAPI().get_contact(contact_id, app_id=app_id)
                assert fetched.contactID == contact_id
                assert fetched.email == payload["Email"]
                assert fetched.firstName == payload["FirstName"]
                assert fetched.lastName == payload["LastName"]

            with allure.step(f"DELETE /subscriptions/{cfg['subscription_id']}/contacts — remove contact"):
                del_response = SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                    int(cfg["subscription_id"]),
                    [contact_id],
                    app_id=app_id,
                )
                assert del_response.status_code in (
                    HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT
                ), f"Delete contact failed: {del_response.status_code} {del_response.text}"
                contact_id = None

        finally:
            if contact_id is not None:
                try:
                    SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                        int(cfg["subscription_id"]),
                        [contact_id],
                        app_id=app_id,
                    )
                except Exception:
                    pass
