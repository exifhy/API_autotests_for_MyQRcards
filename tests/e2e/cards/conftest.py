from http import HTTPStatus

import pytest

from services.attributes.attributes_list.api_attributes_list import AttributesListAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI
from tests.api.conftest import _wait_card_deleted
from src.support.waiter import wait_until


def _delete_leadgen_form_best_effort(account_id: int | None, card_id: int | None, leadgen_form_id: int | None) -> None:
    if not account_id or not card_id or not leadgen_form_id:
        return
    try:
        from services.accounts.accounts_card_leadgen_forms_delete.api_accounts_card_leadgen_forms_delete import (
            AccountsCardLeadGenFormsDeleteAPI,
        )

        AccountsCardLeadGenFormsDeleteAPI().delete_accounts_card_leadgen_forms(
            int(account_id),
            int(card_id),
            [int(leadgen_form_id)],
        )
        deleted = wait_until(
            lambda: _is_leadgen_form_absent(int(account_id), int(card_id), int(leadgen_form_id)),
            timeout_s=60,
            step_s=3,
        )
        assert deleted is True, (
            f"Leadgen form id={leadgen_form_id} is still visible after delete for account_id={account_id}, card_id={card_id}"
        )
    except Exception:
        pass


def _delete_custom_message_templates_best_effort(account_id: int | None, template_ids: list[int] | None) -> None:
    if not account_id or not template_ids:
        return
    try:
        from services.accounts.accounts_custom_message_templates_delete.api_accounts_custom_message_templates_delete import (
            AccountsCustomMessageTemplatesDeleteAPI,
        )

        ids = [int(template_id) for template_id in template_ids if template_id]
        if ids:
            AccountsCustomMessageTemplatesDeleteAPI().delete_accounts_custom_message_templates(int(account_id), ids)
            deleted = wait_until(
                lambda: _are_custom_templates_absent(int(account_id), ids),
                timeout_s=60,
                step_s=3,
            )
            assert deleted is True, (
                f"Custom message templates still visible after delete for account_id={account_id}, ids={ids}"
            )
    except Exception:
        pass


def _is_leadgen_form_absent(account_id: int, card_id: int, leadgen_form_id: int) -> bool | None:
    from services.accounts.accounts_card_leadgen_forms.api_accounts_card_leadgen_forms import (
        AccountsCardLeadGenFormsAPI,
    )

    response, model = AccountsCardLeadGenFormsAPI().get_accounts_card_leadgen_forms(account_id, card_id)
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
        return None
    return True if all(item.id != leadgen_form_id for item in model.items if item.id is not None) else None


def _are_custom_templates_absent(account_id: int, template_ids: list[int]) -> bool | None:
    from services.accounts.accounts_custom_message_templates.api_accounts_custom_message_templates import (
        AccountsCustomMessageTemplatesAPI,
    )

    response, model = AccountsCustomMessageTemplatesAPI().get_accounts_custom_message_templates(account_id)
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
        return None
    present_ids = {int(item.id) for item in model.items if item.id is not None}
    return True if present_ids.isdisjoint({int(template_id) for template_id in template_ids}) else None



@pytest.fixture(scope="session")
def social_attributes_11_37():
    attributes = AttributesListAPI().get_attributes()
    items = [
        {
            "id": int(item.id),
            "name": str(item.name or "").strip(),
        }
        for item in attributes.items.values()
        if item.id is not None and 11 <= int(item.id) <= 37 and str(item.name or "").strip()
    ]
    assert items, "No social attributes found in id range 11..37"
    items.sort(key=lambda item: item["id"])
    return items


@pytest.fixture(scope="module")
def card_leadgen_flow():
    state = {
        "card_id": None,
        "account_id": None,
        "leadgen_form_id": None,
        "leadgen_payload": None,
        "deleted": False,
    }
    yield state

    _delete_leadgen_form_best_effort(
        state.get("account_id"),
        state.get("card_id"),
        state.get("leadgen_form_id"),
    )
    if state.get("card_id") and not state.get("deleted"):
        try:
            CardDeleteByIdAPI().delete_card_by_id(int(state["card_id"]))
            _wait_card_deleted(int(state["card_id"]))
        except Exception:
            pass


@pytest.fixture(scope="module")
def card_leadgen_message_flow():
    state = {
        "card_id": None,
        "account_id": None,
        "leadgen_form_id": None,
        "template_ids": [],
        "template_payload": None,
        "deleted": False,
    }
    yield state

    _delete_leadgen_form_best_effort(
        state.get("account_id"),
        state.get("card_id"),
        state.get("leadgen_form_id"),
    )
    _delete_custom_message_templates_best_effort(
        state.get("account_id"),
        state.get("template_ids"),
    )
    if state.get("card_id") and not state.get("deleted"):
        try:
            CardDeleteByIdAPI().delete_card_by_id(int(state["card_id"]))
            _wait_card_deleted(int(state["card_id"]))
        except Exception:
            pass
