import allure
import pytest
from http import HTTPStatus

from services.contacts.contact_by_id.api_contact_by_id import ContactByIdAPI
from services.contacts.contacts_list.api_contacts_list import ContactsListAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from services.subscriptions.subscription_contacts_update.api_subscription_contacts_update import (
    SubscriptionContactsUpdateAPI,
)
from src.support.waiter import wait_until


@allure.epic("API")
@allure.feature("Contacts")
@pytest.mark.api
@pytest.mark.contacts
class TestContactsFlow:
    @allure.title("GET /accounts/contacts returns list")
    @pytest.mark.smoke
    def test_contacts_list_returns_list(self, contact_api_ctx):
        response, items = ContactsListAPI().get_contacts(app_id=contact_api_ctx["app_id"])

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(items, list)

    @allure.title("Create -> Get -> Update -> Delete contact")
    @pytest.mark.smoke
    def test_contact_crud_flow(self, created_contact):
        contact_id = created_contact["contact_id"]
        app_id = created_contact["app_id"]

        contact = ContactByIdAPI().get_contact(contact_id, app_id=app_id)
        assert contact.contactID == contact_id
        assert contact.email == created_contact["create_payload"]["Email"]
        assert contact.firstName == created_contact["create_payload"]["FirstName"]

        body = {"ContactID": int(contact_id), **created_contact["update_payload"]}
        response = SubscriptionContactsUpdateAPI().update_subscription_contact(
            created_contact["subscription_id"],
            body,
            app_id=app_id,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        def _updated():
            current = ContactByIdAPI().get_contact(contact_id, app_id=app_id)
            return current if current.email == created_contact["update_payload"]["Email"] else None

        updated = wait_until(_updated, timeout_s=60, step_s=3)
        assert updated is not None, "Updated contact was not visible in GET within timeout"
        assert updated.firstName == created_contact["update_payload"]["FirstName"]
        assert updated.lastName == created_contact["update_payload"]["LastName"]

        delete_response = SubscriptionContactsDeleteAPI().delete_subscription_contacts(
            created_contact["subscription_id"],
            [contact_id],
            app_id=app_id,
        )
        assert delete_response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)
        created_contact["contact_id"] = None
