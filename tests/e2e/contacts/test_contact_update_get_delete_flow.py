import allure
import pytest
from http import HTTPStatus

from services.contacts.contact_by_id.api_contact_by_id import ContactByIdAPI
from services.contacts.contact_create_app.api_contact_create_app import ContactCreateAppAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from services.subscriptions.subscription_contacts_update.api_subscription_contacts_update import (
    SubscriptionContactsUpdateAPI,
)
from tests.e2e.contacts.helpers import wait_for_contact


@allure.epic("LK")
@allure.feature("Contacts")
@allure.title("Update contact -> Get -> Delete")
@pytest.mark.contacts
@pytest.mark.e2e
class TestContactUpdateGetDeleteFlow:
    @allure.title("Create contact returns id")
    def test_01_create_contact_returns_id(self, contact_update_flow):
        model = ContactCreateAppAPI().create_contact(
            contact_update_flow["create_payload"],
            app_id=contact_update_flow["application_id"],
        )
        assert model.id, "No id in create response"
        contact_update_flow["contact_id"] = int(model.id)

    @allure.title("Contact GET returns 200")
    def test_02_contact_get_returns_200(self, contact_update_flow):
        contact_id = contact_update_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        data = ContactByIdAPI().get_contact(
            contact_id,
            app_id=contact_update_flow["application_id"],
        )
        assert data.contactID == int(contact_id), "GET contact returned unexpected contact"

    @allure.title("Contact GET contains created fields")
    def test_03_contact_get_contains_created_fields(self, contact_update_flow):
        contact_id = contact_update_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        data = ContactByIdAPI().get_contact(
            contact_id,
            app_id=contact_update_flow["application_id"],
        )

        assert data.email == contact_update_flow["create_payload"]["Email"], "Email mismatch after create"
        assert data.firstName == contact_update_flow["create_payload"]["FirstName"], "FirstName mismatch after create"
        assert data.lastName == contact_update_flow["create_payload"]["LastName"], "LastName mismatch after create"

    @allure.title("Update contact returns success")
    def test_04_update_contact_returns_200(self, contact_update_flow):
        contact_id = contact_update_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        body = {"ContactID": int(contact_id), **contact_update_flow["update_payload"]}
        response = SubscriptionContactsUpdateAPI().update_subscription_contact(
            contact_update_flow["subscription_id"],
            body,
            app_id=contact_update_flow["application_id"],
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Update contact failed: {response.status_code}, body={response.text}"
        )

    @allure.title("Contact GET has updated fields")
    def test_05_contact_get_has_updated_fields(self, contact_update_flow):
        contact_id = contact_update_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        data = wait_for_contact(
            contact_id,
            app_id=contact_update_flow["application_id"],
            email=contact_update_flow["update_payload"]["Email"],
            timeout_s=60,
            step_s=3,
        )
        assert data is not None, "Updated data not visible in GET within timeout"

        assert data.firstName == contact_update_flow["update_payload"]["FirstName"], "FirstName not updated"
        assert data.lastName == contact_update_flow["update_payload"]["LastName"], "LastName not updated"
        assert data.mobilePhone == contact_update_flow["update_payload"]["MobilePhone"], "MobilePhone not updated"

    @allure.title("Delete contact")
    def test_06_delete_contact(self, contact_update_flow):
        contact_id = contact_update_flow["contact_id"]
        assert contact_id, "contact_id empty (test_01 failed?)"

        response = SubscriptionContactsDeleteAPI().delete_subscription_contacts(
            contact_update_flow["subscription_id"],
            [contact_id],
            app_id=contact_update_flow["application_id"],
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Delete contact failed: {response.status_code}, body={response.text}"
        )
        contact_update_flow["deleted"] = True
