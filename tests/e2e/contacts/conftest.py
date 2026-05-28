import time

import pytest

from tests.e2e.contacts.helpers import build_contact_payload, cleanup_contact_state, contacts_app_id


@pytest.fixture(scope="module")
def contact_create_flow(lk_api, cfg, generated_assets):
    photo_path = generated_assets["contact_photo"]
    ctx = {
        "application_id": contacts_app_id(cfg),
        "subscription_id": int(cfg["subscription_id"]),
        "photo_path": photo_path,
        "first_name": "Sber_AT",
        "last_name": "Test_AT",
        "email": f"at_contact_{int(time.time())}@tt.tt",
        "phone": f"+79{int(time.time()) % 1000000000:09d}",
        "attachment_id": None,
        "contact_id": None,
        "deleted": False,
    }

    yield ctx

    if not ctx["deleted"] and ctx["contact_id"]:
        cleanup_contact_state(ctx)

    attachment_id = ctx.get("attachment_id")
    if attachment_id:
        from src.resources.api import delete_attachment

        try:
            delete_attachment(lk_api, int(attachment_id), application_id=ctx["application_id"])
        except Exception:
            pass


@pytest.fixture(scope="module")
def contact_update_flow(cfg):
    create_payload = build_contact_payload("CREATE")
    update_payload = build_contact_payload("UPDATE")

    state = {
        "application_id": contacts_app_id(cfg),
        "subscription_id": int(cfg["subscription_id"]),
        "create_payload": create_payload,
        "update_payload": update_payload,
        "contact_id": None,
        "deleted": False,
    }

    yield state

    cleanup_contact_state(state)


@pytest.fixture(scope="module")
def contact_csv_flow(cfg):
    now = int(time.time())
    state = {
        "application_id": contacts_app_id(cfg),
        "subscription_id": int(cfg["subscription_id"]),
        "contact_id": None,
        "deleted": False,
        "payload": build_contact_payload("CSV", now=now),
    }

    yield state

    cleanup_contact_state(state)
