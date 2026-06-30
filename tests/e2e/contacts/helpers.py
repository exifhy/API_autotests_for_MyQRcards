import time
from http import HTTPStatus

from services.contacts.contact_by_id.api_contact_by_id import ContactByIdAPI
from src.support.helper import Helper
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from src.support.waiter import wait_until


_helper = Helper()


def contacts_app_id(cfg) -> str:
    return str(cfg.get("x_application_id") or "3")


def build_contact_payload(prefix: str, *, now: int | None = None) -> dict:
    ts = now or int(time.time())
    return {
        "FirstName": f"{prefix}_{ts}",
        "LastName": f"Test_{ts}",
        "Email": f"at_contact_{prefix.lower()}_{ts}@tt.tt",
        "MobilePhone": f"+79{ts % 1000000000:09d}",
        "Position": f"Tester_{ts}",
        "CompanyName": f"testcompany_{ts}",
        "Description": f"desc_{ts}",
    }


def cleanup_contact_state(state: dict) -> None:
    try:
        if state.get("contact_id") and not state.get("deleted"):
            SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                state["subscription_id"],
                [state["contact_id"]],
                app_id=state["application_id"],
            )
            wait_contact_absent(
                state["contact_id"],
                app_id=state["application_id"],
            )
    except Exception:
        pass


def wait_for_contact(
    contact_id: int,
    *,
    app_id: str,
    email: str | None = None,
    first_name: str | None = None,
    timeout_s: int = 60,
    step_s: int = 3,
):
    def _present():
        try:
            data = ContactByIdAPI().get_contact(contact_id, app_id=app_id)
        except AssertionError:
            return None
        if email and str(data.email or "").lower() != str(email).lower():
            return None
        if first_name and str(data.firstName or "") != str(first_name):
            return None
        return data

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_contact_absent(
    contact_id: int,
    *,
    app_id: str,
    timeout_s: int = 60,
    step_s: int = 3,
):
    from services.contacts.contact_by_id.endpoints import Endpoints
    from services.contacts.base_api import ContactsBaseAPI

    headers = ContactsBaseAPI().build_headers(app_id=app_id)
    endpoint = Endpoints().get_contact_by_id_endpoint.format(contact_id=int(contact_id))

    def _absent():
        response = _helper._call("GET", url=endpoint, headers=headers)
        if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT):
            return True
        return None

    return wait_until(_absent, timeout_s=timeout_s, step_s=step_s)
