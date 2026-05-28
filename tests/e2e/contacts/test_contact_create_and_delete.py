import allure
import pytest
import time
from http import HTTPStatus

from services.contacts.contact_create_app.api_contact_create_app import ContactCreateAppAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from src.resources.api import delete_attachment
from src.resources.uploads import upload_generated_image
from tests.e2e.contacts.helpers import contacts_app_id, wait_for_contact


@allure.epic("LK")
@allure.feature("Contacts")
@pytest.mark.contacts
@pytest.mark.e2e
@allure.description("/Contacts — upload photo, create, GET verify, delete flow")
class TestContactCreateAndDelete:

    @allure.title("POST /attachments (photo) → POST contact → GET verify → DELETE")
    @pytest.mark.smoke
    def test_contact_create_and_delete_flow(self, lk_api, cfg):
        app_id = contacts_app_id(cfg)
        subscription_id = int(cfg["subscription_id"])
        now = int(time.time())
        attachment_id = None
        contact_id = None
        try:
            with allure.step("01. POST /attachments — upload contact photo (PNG)"):
                attachment_id = upload_generated_image(lk_api, cfg, fmt="png", label="contact photo")
                assert attachment_id > 0, f"Photo attachment id is invalid: {attachment_id}"

            with allure.step("02. POST /contacts — create contact"):
                payload = {
                    "FirstName": "Sber_AT",
                    "LastName": "Test_AT",
                    "Email": f"at_contact_{now}@tt.tt",
                    "MobilePhone": f"+79{now % 1000000000:09d}",
                    "Position": "Tester",
                    "CompanyName": "testcompany",
                    "Description": "desc",
                    "AttachmentID": attachment_id,
                }
                model = ContactCreateAppAPI().create_contact(payload, app_id=app_id)
                assert model.id, "No contact id in create response"
                contact_id = int(model.id)

            with allure.step(f"03. GET /accounts/contacts/{contact_id} — verify contact fields"):
                found = wait_for_contact(
                    contact_id,
                    app_id=app_id,
                    email=payload["Email"],
                    first_name=payload["FirstName"],
                    timeout_s=60,
                    step_s=3,
                )
                assert found is not None, f"Contact id={contact_id} not accessible via GET within 60s"

            with allure.step(f"04. DELETE /subscriptions/{subscription_id}/contacts — remove contact"):
                response = SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                    subscription_id,
                    [contact_id],
                    app_id=app_id,
                )
                assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
                    f"Delete contact failed: {response.status_code} {response.text}"
                )
                contact_id = None

        finally:
            if contact_id is not None:
                try:
                    SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                        subscription_id,
                        [contact_id],
                        app_id=app_id,
                    )
                except Exception:
                    pass
            if attachment_id is not None:
                try:
                    delete_attachment(lk_api, attachment_id, application_id=app_id)
                except Exception:
                    pass
