from pathlib import Path
from http import HTTPStatus

from src.resources.mobile_api import (
    get_mobile_card,
    get_mobile_designsettings,
    list_mobile_card_attributes,
)
from src.support.waiter import wait_until


def list_image_files(folder: str, *, min_count: int = 5) -> list[str]:
    files = [
        str(path)
        for path in sorted(Path(folder).iterdir())
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    assert len(files) >= min_count, f"Need at least {min_count} image files in {folder}, found {len(files)}"
    return files[:min_count]


def extract_mobile_attachment_id(response) -> int:
    data = response.json()
    attachment_id = data.get("id")
    if attachment_id:
        return int(attachment_id)

    attachments = data.get("attachments") or []
    assert attachments, f"No attachments in response: {response.text}"
    attachment_id = attachments[0].get("id")
    assert attachment_id, f"No attachment id in response: {response.text}"
    return int(attachment_id)


def wait_mobile_card_ready(mobile_api, card_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _ok():
        response = get_mobile_card(mobile_api, card_id)
        return response if response.status_code == HTTPStatus.OK else None

    return wait_until(_ok, timeout_s=timeout_s, step_s=step_s)


def wait_mobile_designsettings_ready(mobile_api, card_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _ok():
        response = get_mobile_designsettings(mobile_api, card_id)
        return response if response.status_code == HTTPStatus.OK else None

    return wait_until(_ok, timeout_s=timeout_s, step_s=step_s)


def gallery_contains_all_ids(card_json: dict, expected_ids: list[int]) -> bool:
    gallery = card_json.get("gallery") or []
    if not isinstance(gallery, list):
        return False
    got_ids = []
    for item in gallery:
        if isinstance(item, dict) and "id" in item:
            try:
                got_ids.append(int(item["id"]))
            except Exception:
                continue
    return all(expected_id in got_ids for expected_id in expected_ids)


def gallery_has_attachment_id(card_json: dict, attachment_id: int) -> bool:
    return gallery_contains_all_ids(card_json, [int(attachment_id)])


def deep_contains_value(obj, expected: str) -> bool:
    if obj is None:
        return False
    if isinstance(obj, str):
        return expected in obj
    if isinstance(obj, (int, float, bool)):
        return str(obj) == expected
    if isinstance(obj, list):
        return any(deep_contains_value(item, expected) for item in obj)
    if isinstance(obj, dict):
        return any(deep_contains_value(value, expected) for value in obj.values())
    return False


def find_attr_by_name(items: list[dict], name: str) -> dict | None:
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("name") == name:
            return item
        if isinstance(item.get("attribute"), dict) and item["attribute"].get("name") == name:
            return item
        if isinstance(item.get("cardAttribute"), dict) and item["cardAttribute"].get("name") == name:
            return item
        if deep_contains_value(item, name):
            return item
    return None


def find_attr_by_value(items: list[dict], expected_value: str) -> dict | None:
    expected = str(expected_value)
    for item in items:
        if deep_contains_value(item, expected):
            return item
    return None


def find_enabled_attr(items: list[dict], *, expected_value: str) -> dict | None:
    expected = str(expected_value)
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("isEnabled") is True:
            values = item.get("values")
            if isinstance(values, list) and any(str(value) == expected for value in values):
                return item
            if deep_contains_value(item, expected):
                return item
    return None


def attr_values_flat(attr_obj: dict) -> list[str]:
    if not isinstance(attr_obj, dict):
        return []
    values = attr_obj.get("values", attr_obj.get("Values"))
    if not isinstance(values, list):
        return []
    return [str(value) for value in values]


def wait_mobile_gallery_contains(
    mobile_api,
    card_id: int,
    expected_ids: list[int],
    *,
    timeout_s: int = 60,
    step_s: int = 3,
):
    def _present():
        response = wait_mobile_card_ready(mobile_api, card_id, timeout_s=timeout_s, step_s=step_s)
        card_json = response.json()
        return card_json if gallery_contains_all_ids(card_json, expected_ids) else None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_mobile_gallery_has_attachment(
    mobile_api,
    card_id: int,
    attachment_id: int,
    *,
    timeout_s: int = 90,
    step_s: int = 3,
):
    def _present():
        response = wait_mobile_card_ready(mobile_api, card_id, timeout_s=timeout_s, step_s=step_s)
        card_json = response.json()
        return card_json if gallery_has_attachment_id(card_json, attachment_id) else None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_mobile_designsettings_contains(
    mobile_api,
    card_id: int,
    expected_value,
    *,
    timeout_s: int = 60,
    step_s: int = 3,
):
    expected = str(expected_value)

    def _present():
        response = wait_mobile_designsettings_ready(mobile_api, card_id, timeout_s=timeout_s, step_s=step_s)
        data = response.json()
        return data if deep_contains_value(data, expected) else None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_mobile_attr_values(
    mobile_api,
    card_id: int,
    *,
    expected_values: list[str],
    attribute_id: int | None = None,
    expected_name: str | None = None,
    enabled_only: bool = False,
    timeout_s: int = 60,
    step_s: int = 3,
):
    expected = [str(value) for value in expected_values]

    def _present():
        params = {"attributeID": str(attribute_id)} if attribute_id is not None else None
        response = list_mobile_card_attributes(mobile_api, card_id, params=params)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json()
        if not isinstance(items, list):
            return None

        matched = None
        for value in expected:
            item = find_enabled_attr(items, expected_value=value) if enabled_only else find_attr_by_value(items, value)
            if not item:
                return None
            matched = item

        if expected_name is not None and find_attr_by_name(items, expected_name) is None:
            return None
        return items if matched else None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)
