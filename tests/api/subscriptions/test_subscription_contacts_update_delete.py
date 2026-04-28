import time

import allure
import pytest
from http import HTTPStatus

from services.contacts.contact_create_app.api_contact_create_app import ContactCreateAppAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from services.subscriptions.subscription_contacts_update.api_subscription_contacts_update import (
    SubscriptionContactsUpdateAPI,
)


def _app_id(cfg) -> str:
    return str(cfg.get("x_application_id") or "3")


def _contact_payload(prefix: str) -> dict:
    ts = int(time.time())
    return {
        "FirstName": f"{prefix}_{ts}",
        "LastName": f"Test_{ts}",
        "Email": f"at_contact_{prefix.lower()}_{ts}@tt.tt",
        "MobilePhone": f"+79{ts % 1000000000:09d}",
        "Position": f"Tester_{ts}",
        "CompanyName": f"testcompany_{ts}",
    }


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    611 PUT    /subscriptions/{id}/contacts
    612 DELETE /subscriptions/{id}/contacts
    """
)
class TestSubscriptionContactsUpdateDelete:
    @allure.title("611+612: POST contact -> PUT update -> DELETE from subscription")
    def test_subscription_contacts_update_delete_flow(self, cfg):
        sub_id = int(cfg["subscription_id"])
        app_id = _app_id(cfg)
        contact_id = None

        try:
            with allure.step("POST /accounts/contacts/app — create contact"):
                created = ContactCreateAppAPI().create_contact(
                    _contact_payload("AT_611"),
                    app_id=app_id,
                )
                assert created.id is not None, "Created contact has no id"
                contact_id = int(created.id)

            with allure.step(f"611 PUT /subscriptions/{sub_id}/contacts — update contact"):
                update_payload = {
                    "ContactID": contact_id,
                    **_contact_payload("AT_611_UPD"),
                }
                upd_response = SubscriptionContactsUpdateAPI().update_subscription_contact(
                    sub_id,
                    update_payload,
                    app_id=app_id,
                )
                assert upd_response.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.ACCEPTED,
                    HTTPStatus.NO_CONTENT,
                )

            with allure.step(f"612 DELETE /subscriptions/{sub_id}/contacts — remove contact from subscription"):
                del_response = SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                    sub_id,
                    [contact_id],
                    app_id=app_id,
                )
                assert del_response.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.ACCEPTED,
                    HTTPStatus.NO_CONTENT,
                )
                contact_id = None

        finally:
            if contact_id:
                try:
                    SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                        sub_id,
                        [contact_id],
                        app_id=app_id,
                    )
                except Exception:
                    pass
