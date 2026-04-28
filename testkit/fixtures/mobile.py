import time

import pytest

from src.resources.mobile_api import (
    MobileApiClient,
    delete_mobile_attachment_with_retry,
    delete_mobile_card_with_retry,
)
from tests.e2e.mobile.builders import build_mobile_payload, build_mobile_random_payload


@pytest.fixture(scope="session")
def mobile_api(cfg) -> MobileApiClient:
    token = cfg.get("mobile_jwt") or cfg.get("lk_jwt")
    assert token, "No token available for mobile_api (MOBILE_JWT and LK_JWT are both missing)"
    return MobileApiClient(host=cfg["host"], token=token)


def _build_mobile_flow(*, payload: dict, media: dict | None = None, expected: dict | None = None, **extra) -> dict:
    state = {
        "payload": payload,
        "card_id": None,
        "deleted": False,
        "media": media or {},
        "expected": expected or {},
    }
    state.update(extra)
    return state


def _safe_cleanup_mobile_flow(mobile_api: MobileApiClient, state: dict) -> None:
    errors: list[str] = []

    card_id = state.get("card_id")
    leadgen_form_id = state.get("leadgen_form_id")
    if card_id and leadgen_form_id:
        try:
            from services.cards.card_leadgen_forms_delete.api_card_leadgen_forms_delete import (
                CardLeadGenFormsDeleteAPI,
            )

            CardLeadGenFormsDeleteAPI().delete_card_leadgen_forms(int(card_id), [int(leadgen_form_id)])
        except Exception as exc:
            errors.append(f"leadgen form cleanup failed for card_id={card_id}, leadgen_form_id={leadgen_form_id}: {exc}")

    if card_id and not state.get("deleted"):
        try:
            response = delete_mobile_card_with_retry(mobile_api, int(card_id))
            status = getattr(response, "status_code", None)
            if status not in (200, 202, 204, 404, 410):
                errors.append(f"mobile card cleanup failed for card_id={card_id}: status={status}")
        except Exception as exc:
            errors.append(f"mobile card cleanup failed for card_id={card_id}: {exc}")

    attachment_keys = (
        "attachment_id",
        "doc_attachment_id",
        "avatar_attachment_id",
        "banner_attachment_id",
        "background_attachment_id",
    )
    for key in attachment_keys:
        attachment_id = state.get(key)
        if attachment_id:
            try:
                response = delete_mobile_attachment_with_retry(mobile_api, int(attachment_id))
                status = getattr(response, "status_code", None)
                if status not in (200, 202, 204, 404, 410):
                    errors.append(f"mobile attachment cleanup failed for {key}={attachment_id}: status={status}")
            except Exception as exc:
                errors.append(f"mobile attachment cleanup failed for {key}={attachment_id}: {exc}")

    for attachment_id in state.get("uploaded_ids", []) or []:
        if attachment_id:
            try:
                response = delete_mobile_attachment_with_retry(mobile_api, int(attachment_id))
                status = getattr(response, "status_code", None)
                if status not in (200, 202, 204, 404, 410):
                    errors.append(f"mobile uploaded attachment cleanup failed for attachment_id={attachment_id}: status={status}")
            except Exception as exc:
                errors.append(f"mobile uploaded attachment cleanup failed for attachment_id={attachment_id}: {exc}")

    if errors:
        raise AssertionError("Mobile cleanup issues:\n" + "\n".join(errors))


@pytest.fixture(scope="module")
def mobile_card_create_flow(mobile_api, generated_assets):
    photo_path = generated_assets["mobile_image"]
    now = int(time.time())
    state = _build_mobile_flow(
        payload=build_mobile_payload(now=now),
        media={"photo_path": photo_path},
        expected={
            "phone": "84654563535",
            "email": "kakdela@gmail.com",
        },
        attachment_id=None,
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)


@pytest.fixture(scope="module")
def mobile_avatar_gallery_flow(mobile_api, generated_assets):
    photos_dir = generated_assets["photos_dir"]
    now = int(time.time())
    state = _build_mobile_flow(
        payload=build_mobile_payload(now=now),
        media={"photos_dir": photos_dir},
        uploaded_ids=[],
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)


@pytest.fixture(scope="module")
def mobile_tg_wa_flow(mobile_api):
    now = int(time.time())
    payload = build_mobile_payload(now=now)
    payload["Person"]["Attachments"] = None
    state = _build_mobile_flow(
        payload=payload,
        expected={
            "tg": "89454531212",
            "wa": "89990002211",
        },
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)


@pytest.fixture(scope="module")
def mobile_file_flow(mobile_api, generated_assets):
    now = int(time.time())
    doc_path = generated_assets["import_xlsx"]
    photo_path = generated_assets["mobile_image"]

    state = _build_mobile_flow(
        payload=build_mobile_payload(now=now, name_prefix="MobileCard"),
        media={
            "photo_path": photo_path,
            "doc_path": doc_path,
        },
        expected={
            "phone": "84654563535",
            "email": "kakdela@gmail.com",
        },
        attachment_id=None,
        doc_attachment_id=None,
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)


@pytest.fixture(scope="module")
def mobile_avatar_photo_flow(mobile_api, generated_assets):
    now = int(time.time())
    photos_dir = generated_assets["photos_dir"]
    photo_paths = generated_assets["photo_paths"]

    state = _build_mobile_flow(
        payload=build_mobile_payload(now=now),
        media={
            "photos_dir": photos_dir,
            "photo_paths": photo_paths,
        },
        uploaded_ids=[],
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)


@pytest.fixture(scope="module")
def mobile_avatar_text_banner_flow(mobile_api, generated_assets):
    photo_path = generated_assets["mobile_image"]
    state = _build_mobile_flow(
        payload=build_mobile_random_payload(name_prefix="Card"),
        media={"photo_path": photo_path},
        avatar_attachment_id=None,
        text_value=None,
        banner_attachment_id=None,
        banner_url=None,
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)


@pytest.fixture(scope="module")
def mobile_back_color_youtube_flow(mobile_api, generated_assets):
    back_path = generated_assets["back_image"]
    state = _build_mobile_flow(
        payload=build_mobile_random_payload(name_prefix="TestCard"),
        media={"back_path": back_path},
        expected={"base_color": "4673B4"},
        background_attachment_id=None,
        color_2=None,
        youtube_url=None,
    )
    yield state
    _safe_cleanup_mobile_flow(mobile_api, state)
