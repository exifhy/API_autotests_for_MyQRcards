import time
from http import HTTPStatus

import pytest

from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from src.support.helper import Helper
from services.cards.card_leadgen_forms_delete.api_card_leadgen_forms_delete import (
    CardLeadGenFormsDeleteAPI,
)
from services.contacts.contact_create_app.api_contact_create_app import ContactCreateAppAPI
from services.subscriptions.subscription_contacts_delete.api_subscription_contacts_delete import (
    SubscriptionContactsDeleteAPI,
)
from src.support.waiter import wait_until

_helper = Helper()


def _wait_contact_deleted(contact_id: int, *, app_id: str, timeout_s: int = 60, step_s: int = 3) -> bool:
    from services.contacts.contact_by_id.endpoints import Endpoints
    from services.contacts.base_api import ContactsBaseAPI

    headers = ContactsBaseAPI().build_headers(app_id=app_id)
    endpoint = Endpoints().get_contact_by_id_endpoint.format(contact_id=int(contact_id))

    def _gone():
        response = _helper._call("GET", url=endpoint, headers=headers)
        if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND):
            return True
        return None

    return bool(wait_until(_gone, timeout_s=timeout_s, step_s=step_s))


@pytest.fixture
def contact_api_ctx(cfg):
    now = int(time.time())
    state = {
        "app_id": str(cfg.get("x_application_id") or "3"),
        "subscription_id": int(cfg["subscription_id"]),
        "contact_id": None,
        "create_payload": {
            "FirstName": f"Api_{now}",
            "LastName": f"Contact_{now}",
            "Email": f"api_contact_{now}@tt.tt",
            "MobilePhone": f"+79{now % 1000000000:09d}",
            "Position": f"Tester_{now}",
            "CompanyName": f"Company_{now}",
            "Description": f"Desc_{now}",
        },
        "update_payload": {
            "FirstName": f"ApiUpd_{now}",
            "LastName": f"ContactUpd_{now}",
            "Email": f"api_contact_upd_{now}@tt.tt",
            "MobilePhone": f"+79{(now + 1) % 1000000000:09d}",
            "Position": f"TesterUpd_{now}",
            "CompanyName": f"CompanyUpd_{now}",
            "Description": f"DescUpd_{now}",
        },
    }

    yield state

    if state["contact_id"]:
        try:
            SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                state["subscription_id"],
                [state["contact_id"]],
                app_id=state["app_id"],
            )
            _wait_contact_deleted(state["contact_id"], app_id=state["app_id"])
        except Exception:
            pass


@pytest.fixture
def created_contact(contact_api_ctx):
    model = ContactCreateAppAPI().create_contact(
        contact_api_ctx["create_payload"],
        app_id=contact_api_ctx["app_id"],
    )
    assert model.id, "Contact create did not return id"
    contact_api_ctx["contact_id"] = int(model.id)
    return contact_api_ctx


@pytest.fixture
def web_contact_ctx(cfg):
    now = int(time.time())
    state = {
        "app_id": str(cfg.get("x_application_id") or "3"),
        "subscription_id": int(cfg["subscription_id"]),
        "card_id": None,
        "leadgen_form_id": None,
        "contact_id": None,
        "payload": {
            "FirstName": f"Web_{now}",
            "LastName": f"Contact_{now}",
            "Email": f"web_contact_{now}@tt.tt",
            "MobilePhone": f"+79{now % 1000000000:09d}",
            "Position": f"Tester_{now}",
            "CompanyName": f"Company_{now}",
            "Description": f"Desc_{now}",
        },
    }

    yield state

    if state["contact_id"]:
        try:
            SubscriptionContactsDeleteAPI().delete_subscription_contacts(
                state["subscription_id"],
                [state["contact_id"]],
                app_id=state["app_id"],
            )
            _wait_contact_deleted(state["contact_id"], app_id=state["app_id"])
        except Exception:
            pass

    if state["leadgen_form_id"] and state["card_id"]:
        try:
            CardLeadGenFormsDeleteAPI().delete_card_leadgen_forms(state["card_id"], [state["leadgen_form_id"]])
        except Exception:
            pass

    if state["card_id"]:
        try:
            CardDeleteByIdAPI().delete_card_by_id(state["card_id"])
        except Exception:
            pass
