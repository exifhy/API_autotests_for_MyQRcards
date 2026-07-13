from http import HTTPStatus

from services.subscriptions.subscription_moderators_list.api_subscription_moderators_list import (
    SubscriptionModeratorsListAPI,
)
from src.constants.attributes import PHOTO_GALLERY_ATTRIBUTE_ID
from src.resources.api import accounts_list
from src.resources.helpers import find_account_in_list
from src.support.waiter import wait_until


def accounts_list_all(lk_api):
    return lk_api.get("/accounts", params={"IsIncludeSubscriptionOwner": "true"})


def accounts_list_by_company(lk_api, company_id: int):
    return lk_api.get(
        "/accounts",
        params={
            "IsIncludeSubscriptionOwner": "true",
            "companyID": str(company_id),
        },
    )


def get_accounts_json_safe(response):
    if response.status_code == HTTPStatus.NO_CONTENT:
        return []
    if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
        return None
    try:
        data = response.json()
    except Exception:
        return None
    return data if isinstance(data, list) else None


def find_account_by_first_name(items: list, first_name: str):
    for item in items or []:
        if (item.get("firstName") or "") == first_name:
            return item
    return None


def wait_for_account_present(lk_api, account_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _present():
        response = accounts_list(lk_api, account_id=account_id)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json()
        if not isinstance(items, list):
            return None
        return find_account_in_list(items, account_id)

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_for_account_hidden_state(
    lk_api,
    account_id: int,
    *,
    is_hidden: bool,
    timeout_s: int = 90,
    step_s: int = 5,
):
    def _state():
        response = accounts_list(lk_api, account_id=account_id)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json()
        if not isinstance(items, list):
            return None
        obj = find_account_in_list(items, account_id)
        if not obj:
            return None
        return True if obj.get("isHidden") is is_hidden else None

    return wait_until(_state, timeout_s=timeout_s, step_s=step_s)


def wait_for_all_first_names_present(
    lk_api,
    first_names: list[str],
    *,
    company_id: int | None = None,
    timeout_s: int = 90,
    step_s: int = 5,
):
    def _present_all():
        response = accounts_list_by_company(lk_api, company_id) if company_id is not None else accounts_list_all(lk_api)
        items = get_accounts_json_safe(response)
        if items is None:
            return None
        for first_name in first_names:
            if find_account_by_first_name(items, first_name) is None:
                return None
        return True

    return wait_until(_present_all, timeout_s=timeout_s, step_s=step_s)


def wait_for_all_account_ids_present(
    lk_api,
    account_ids: set[int],
    *,
    timeout_s: int = 90,
    step_s: int = 3,
):
    def _present_all():
        response = accounts_list(lk_api)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json()
        if not isinstance(items, list):
            return None
        found = {int(it.get("id")) for it in items if it.get("id") is not None}
        return True if account_ids.issubset(found) else None

    return wait_until(_present_all, timeout_s=timeout_s, step_s=step_s)


def wait_for_all_account_ids_present_in_company(
    lk_api,
    account_ids: set[int],
    *,
    company_id: int,
    timeout_s: int = 90,
    step_s: int = 5,
):
    def _present_all():
        response = accounts_list_by_company(lk_api, company_id)
        items = get_accounts_json_safe(response)
        if items is None:
            return None
        found = {int(it.get("id")) for it in items if it.get("id") is not None}
        return True if account_ids.issubset(found) else None

    return wait_until(_present_all, timeout_s=timeout_s, step_s=step_s)


def wait_for_all_account_ids_absent_in_company(
    lk_api,
    account_ids: set[int],
    *,
    company_id: int,
    timeout_s: int = 120,
    step_s: int = 5,
):
    def _gone():
        response = accounts_list_by_company(lk_api, company_id)
        if response.status_code == HTTPStatus.NO_CONTENT:
            return True
        items = get_accounts_json_safe(response)
        if items is None:
            return None
        found = {int(it.get("id")) for it in items if it.get("id") is not None}
        return True if account_ids.isdisjoint(found) else None

    return wait_until(_gone, timeout_s=timeout_s, step_s=step_s)


def wait_for_all_first_names_absent_in_company(
    lk_api,
    first_names: list[str],
    *,
    company_id: int,
    timeout_s: int = 120,
    step_s: int = 5,
):
    def _gone():
        response = accounts_list_by_company(lk_api, company_id)
        if response.status_code == HTTPStatus.NO_CONTENT:
            return True
        items = get_accounts_json_safe(response)
        if items is None:
            return None
        for first_name in first_names:
            if find_account_by_first_name(items, first_name) is not None:
                return None
        return True

    return wait_until(_gone, timeout_s=timeout_s, step_s=step_s)


def find_account_in_moderators(items: list, account_id: int):
    for item in items or []:
        if isinstance(item, dict) and int(item.get("accountID", -1)) == int(account_id):
            return item
    return None


def wait_for_moderator_present(
    lk_api,
    *,
    sub_id: int,
    account_id: int,
    timeout_s: int = 120,
    step_s: int = 5,
):
    def _present():
        _, model = SubscriptionModeratorsListAPI().get_subscription_moderators(sub_id)
        items = [item.model_dump() for item in model.items]
        return find_account_in_moderators(items, account_id)

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def wait_for_moderator_absent(
    lk_api,
    *,
    sub_id: int,
    account_id: int,
    timeout_s: int = 120,
    step_s: int = 5,
):
    def _absent():
        _, model = SubscriptionModeratorsListAPI().get_subscription_moderators(sub_id)
        items = [item.model_dump() for item in model.items]
        return True if find_account_in_moderators(items, account_id) is None else None

    return wait_until(_absent, timeout_s=timeout_s, step_s=step_s)


def get_card_attributes_0852(lk_api, account_id: int, card_id: int = 1):
    return lk_api.get(f"/accounts/{account_id}/cards/{card_id}/attributes/")


def has_photo_attr_with_values(items: list, attachment_ids: list[int]) -> bool:
    need = {str(x) for x in attachment_ids}

    for item in items:
        if not isinstance(item, dict):
            continue

        attr = item.get("attribute") or {}
        if int(attr.get("id", -1)) != int(PHOTO_GALLERY_ATTRIBUTE_ID):
            continue

        values = item.get("values") or []
        got = {str(value) for value in values if value is not None}
        return need.issubset(got)

    return False


def wait_for_photo_attr_in_0852(
    lk_api,
    *,
    account_id: int,
    card_id: int,
    attachment_ids: list[int],
    timeout_s: int = 120,
    step_s: int = 5,
):
    def _ok():
        response = get_card_attributes_0852(lk_api, account_id, card_id=card_id)
        if response.status_code != HTTPStatus.OK:
            return None
        data = response.json()
        if not isinstance(data, list):
            return None
        return True if has_photo_attr_with_values(data, attachment_ids) else None

    return wait_until(_ok, timeout_s=timeout_s, step_s=step_s)


def extract_emails(resp_json):
    if not isinstance(resp_json, list):
        return set()
    emails = set()
    for item in resp_json:
        if isinstance(item, dict):
            email = item.get("email") or item.get("Email")
            if email:
                emails.add(str(email).lower())
    return emails


def extract_ids(resp_json):
    if not isinstance(resp_json, list):
        return set()
    ids = set()
    for item in resp_json:
        if isinstance(item, dict):
            account_id = item.get("id") or item.get("ID")
            if account_id is not None:
                try:
                    ids.add(int(account_id))
                except (TypeError, ValueError):
                    pass
    return ids
