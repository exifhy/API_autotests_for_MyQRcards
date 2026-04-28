from http import HTTPStatus
from src.api.endpoints import (
    CARD_ATTRIBUTES_LIST_0852_PATH,
    CARD_ATTRIBUTES_MERGE_PATH,
    CARD_V2_PATH,
    EXPORTS_EMPLOYMENT_PATH,
    SUBSCRIPTION_MODERATOR_GET_PATH,
    SUBSCRIPTION_MODERATORS_ADD_PATH,
)
from src.resources.helpers import parse_card_v2_minimal


def accounts_list(lk_api, account_id: int | None = None):
    params = {"IsIncludeSubscriptionOwner": "true"}
    if account_id is not None:
        params["accountID"] = str(account_id)
    return lk_api.get("/accounts", params=params)


def companies_list(lk_api):
    return lk_api.get("/companies")


def get_company_json(lk_api, company_id: int) -> dict | None:
    response = lk_api.get(f"/companies/{int(company_id)}")
    return response.json() if response.status_code == HTTPStatus.OK and response.text else None


def get_designsettings_json(lk_api, company_id: int) -> dict | None:
    response = lk_api.get(f"/companies/{int(company_id)}/designsettings")
    return response.json() if response.status_code == HTTPStatus.OK and response.text else None


def get_card_v2_by_account(lk_api, *, account_id: int, card_id: int = 1):
    from services.accounts.accounts_card_by_id_v2.api_accounts_card_by_id_v2 import AccountsCardByIdV2API

    response, _ = AccountsCardByIdV2API().get_accounts_card_by_id_v2(
        int(account_id),
        int(card_id),
    )
    return response


def get_card_v2_raw(lk_api, card_id: int):
    path = CARD_V2_PATH.format(card_id=int(card_id))
    return lk_api.get(path)


def merge_card_attributes(lk_api, *, account_id: int, card_id: int, body: list[dict]):
    path = CARD_ATTRIBUTES_MERGE_PATH.format(account_id=int(account_id), card_id=int(card_id))
    return lk_api.put(path, json=body)


def list_card_attributes_0852(lk_api, *, account_id: int, card_id: int):
    path = CARD_ATTRIBUTES_LIST_0852_PATH.format(account_id=int(account_id), card_id=int(card_id))
    return lk_api.get(path)


def add_moderator(lk_api, *, sub_id: int, account_id: int):
    path = SUBSCRIPTION_MODERATORS_ADD_PATH.format(sub_id=int(sub_id))
    return lk_api.post(path, json=[int(account_id)])


def get_moderator(lk_api, *, sub_id: int, account_id: int):
    path = SUBSCRIPTION_MODERATOR_GET_PATH.format(sub_id=int(sub_id), account_id=int(account_id))
    return lk_api.get(path)


def list_moderators(lk_api, *, sub_id: int):
    return lk_api.get(f"/subscriptions/{int(sub_id)}/moderators")


def delete_moderator(lk_api, *, sub_id: int, account_id: int):
    path = f"/subscriptions/{int(sub_id)}/moderators"
    variants = [
        [int(account_id)],
        {"accountID": [int(account_id)]},
        {"accountID": int(account_id)},
    ]
    last = None
    for body in variants:
        last = lk_api.delete(path, json=body)
        if last.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT):
            return last
    return last


def hide_cards(lk_api, body: list[dict]):
    return lk_api.put("/cards/hide", json=body)


def show_cards(lk_api, body: list[dict]):
    return lk_api.put("/cards/show", json=body)


def copy_cards_to_company(lk_api, items: list[dict]):
    return lk_api.post("/cards/card/copy", json=items)


def patch_card_v2(lk_api, *, account_id: int, card_id: int, body: list[dict]):
    from services.accounts.accounts_card_patch_v2.api_accounts_card_patch_v2 import AccountsCardPatchV2API

    return AccountsCardPatchV2API().patch_accounts_card_v2(
        int(account_id),
        int(card_id),
        body,
    )


def upload_attachment(lk_api, *, file_path: str, application_id: str | None = None):
    headers = dict(lk_api.session.headers)
    headers.pop("Content-Type", None)
    headers["Accept"] = "*/*"
    if application_id:
        headers["X-Aplication-ID"] = str(application_id)

    import mimetypes
    import os

    filename = os.path.basename(file_path)
    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "application/octet-stream"

    with open(file_path, "rb") as file:
        return lk_api.session.post(
            lk_api.base_url + "/attachments",
            files={"File": (filename, file, mime)},
            headers=headers,
            allow_redirects=True,
            timeout=30,
        )


def delete_attachment(lk_api, attachment_id: int, application_id: str | None = None):
    headers = dict(lk_api.session.headers)
    headers["Accept"] = "application/json"
    if application_id:
        headers["X-Aplication-ID"] = str(application_id)
    return lk_api.session.delete(
        lk_api.base_url + f"/attachments/{int(attachment_id)}",
        headers=headers,
        allow_redirects=True,
        timeout=30,
    )


def create_contact_app(lk_api, payload: dict, application_id: str | None = None):
    headers = dict(lk_api.session.headers)
    headers.pop("Content-Type", None)
    headers["Accept"] = "application/json"
    if application_id:
        headers["X-Aplication-ID"] = str(application_id)
    return lk_api.session.post(
        lk_api.base_url + "/accounts/contacts/app",
        json=payload,
        headers=headers,
        allow_redirects=True,
        timeout=30,
    )


def get_contact(lk_api, contact_id: int, application_id: str | None = None):
    headers = dict(lk_api.session.headers)
    headers["Accept"] = "application/json"
    if application_id:
        headers["X-Aplication-ID"] = str(application_id)
    return lk_api.session.get(
        lk_api.base_url + f"/accounts/contacts/{int(contact_id)}",
        headers=headers,
        allow_redirects=True,
        timeout=30,
    )


def update_contact(lk_api, payload: dict):
    response = lk_api.put("/accounts/contacts", json=payload)
    if response.status_code in (HTTPStatus.NOT_FOUND, 405):
        response = lk_api.post("/accounts/contacts", json=payload)
    return response


def delete_contacts(lk_api, subscription_id: int, contact_ids: list[int], application_id: str | None = None):
    headers = dict(lk_api.session.headers)
    headers["Accept"] = "application/json"
    if application_id:
        headers["X-Aplication-ID"] = str(application_id)
    return lk_api.session.delete(
        lk_api.base_url + f"/subscriptions/{int(subscription_id)}/contacts",
        json=[int(contact_id) for contact_id in contact_ids],
        headers=headers,
        allow_redirects=True,
        timeout=30,
    )


def download_contacts_csv(lk_api, subscription_id: int, date_from: str, date_till: str):
    headers = dict(lk_api.session.headers)
    headers.pop("Content-Type", None)
    headers["Accept"] = "*/*"
    return lk_api.session.get(
        lk_api.base_url + f"/Subscriptions/{int(subscription_id)}/contacts/download",
        params={"DateFrom": date_from, "DateTill": date_till},
        headers=headers,
        allow_redirects=True,
        timeout=30,
    )


def get_card_v2_minimal(lk_api, card_id: int) -> dict | None:
    response = get_card_v2_raw(lk_api, card_id)
    if response.status_code != HTTPStatus.OK:
        return None
    data = response.json() if response.text else {}
    return parse_card_v2_minimal(data)


def export_employment(lk_api):
    return lk_api.get(EXPORTS_EMPLOYMENT_PATH)
