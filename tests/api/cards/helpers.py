import requests
from http import HTTPStatus

from services.cards.card_attachments_sortorder.api_card_attachments_sortorder import (
    CardAttachmentsSortOrderAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_by_id_v2.api_card_by_id_v2 import CardByIdV2API
from services.cards.card_leadgen_forms_create.api_card_leadgen_forms_create import (
    CardLeadGenFormsCreateAPI,
)
from services.cards.card_leadgen_forms_delete.api_card_leadgen_forms_delete import (
    CardLeadGenFormsDeleteAPI,
)
from src.support.waiter import wait_until


def extract_card_link_id(card_url: str) -> str:
    return card_url.rstrip("/").split("/")[-1]


def extract_account_uri_name(account_url: str) -> str:
    return account_url.rstrip("/").split("/")[-1]


def gallery_ids(card_json) -> list[int]:
    gallery = card_json.gallery or []
    return [int(item["id"]) for item in gallery if isinstance(item, dict) and item.get("id") is not None]


def wait_card_hidden_state(card_id: int, expected_hidden: bool, *, timeout_s: int = 60, step_s: int = 3):
    def _state():
        fetched = CardByIdAPI().get_card_by_id(card_id)
        return fetched if fetched.isHidden is expected_hidden else None

    return wait_until(_state, timeout_s=timeout_s, step_s=step_s)


def wait_card_v2_gallery_contains(card_id: int, attachment_ids: list[int], *, timeout_s: int = 60, step_s: int = 3):
    expected_ids = {int(item_id) for item_id in attachment_ids}

    def _gallery_present():
        try:
            fetched = CardByIdV2API().get_card_by_id_v2(card_id)
        except requests.RequestException:
            return None
        got_ids = set(gallery_ids(fetched))
        return fetched if got_ids >= expected_ids else None

    return wait_until(_gallery_present, timeout_s=timeout_s, step_s=step_s)


def wait_card_attachments_sortorder(card_id: int, expected: dict[int, int], *, timeout_s: int = 60, step_s: int = 3):
    expected_map = {int(attachment_id): int(sort_order) for attachment_id, sort_order in expected.items()}

    def _sortorder_updated():
        try:
            _, fetched_items = CardAttachmentsSortOrderAPI().get_card_attachments_sortorder(card_id)
        except requests.RequestException:
            return None
        matched = {
            item.attachmentID: item.sortOrder
            for item in fetched_items
            if item.attachmentID in expected_map
        }
        return matched if matched == expected_map else None

    return wait_until(_sortorder_updated, timeout_s=timeout_s, step_s=step_s)


def get_card_account_id(card_id: int) -> int:
    card = CardByIdAPI().get_card_by_id(card_id)
    assert card.accountID is not None, "Card accountID is empty"
    return int(card.accountID)


def create_card_leadgen_form(
    card_id: int,
    *,
    field_template_id: int,
    custom_message_template_id: int | None = None,
) -> int:
    created_form = CardLeadGenFormsCreateAPI().create_card_leadgen_form(
        card_id,
        field_template_id=field_template_id,
        custom_message_template_id=custom_message_template_id,
    )
    assert created_form.id is not None
    return int(created_form.id)


def delete_card_leadgen_form_best_effort(card_id: int, leadgen_form_id: int | None) -> None:
    if leadgen_form_id is None:
        return
    try:
        CardLeadGenFormsDeleteAPI().delete_card_leadgen_forms(card_id, [int(leadgen_form_id)])
        deleted = wait_until(
            lambda: _is_card_leadgen_form_absent(card_id, int(leadgen_form_id)),
            timeout_s=60,
            step_s=3,
        )
        assert deleted is True, f"Leadgen form id={leadgen_form_id} is still visible after delete for card_id={card_id}"
    except Exception:
        pass


def _is_card_leadgen_form_absent(card_id: int, leadgen_form_id: int) -> bool | None:
    response, model = CardLeadGenFormsAPI().get_card_leadgen_forms(card_id)
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
        return None
    return True if all(item.id != leadgen_form_id for item in model.items if item.id is not None) else None


def assert_card_designsettings_match(fetched, payload: dict, *, card_id: int) -> None:
    assert fetched.cardID == card_id
    assert fetched.color == payload["color"]
    assert fetched.qrColor == payload["qrColor"]
    assert fetched.backgroundColor == payload["backgroundColor"]
    assert fetched.foregroundColor == payload["foregroundColor"]


def assert_card_basic(fetched, *, card_id: int) -> None:
    assert fetched.id == card_id
    if hasattr(fetched, "name"):
        assert fetched.name is None or fetched.name != ""
    if hasattr(fetched, "accountID"):
        assert fetched.accountID is not None
    assert fetched.person is not None


def assert_card_full(fetched, *, card_id: int) -> None:
    assert_card_basic(fetched, card_id=card_id)
    assert fetched.subscription is not None
    assert fetched.cardTheme is not None


def assert_card_update_match(fetched, payload: dict, *, card_id: int) -> None:
    assert fetched.id == card_id
    assert fetched.name == payload["name"]
    assert fetched.culture == payload["culture"]
    assert fetched.isPrimary == payload["isPrimary"]
    assert fetched.person is not None
    assert fetched.person.firstName == payload["person"]["firstName"]
    assert fetched.person.lastName == payload["person"]["lastName"]
    assert fetched.person.middleName == payload["person"]["middleName"]
    assert fetched.cardTheme is not None
