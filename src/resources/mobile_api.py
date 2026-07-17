from __future__ import annotations
from http import HTTPStatus

import allure
import mimetypes
import os
import time

import requests

from src.support.helper import Helper


class MobileApiClient:
    def __init__(self, host: str, token: str):
        self.base_url = host.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kwargs):
        url = self.base_url + path
        with allure.step(f"{method.upper()} {path}"):
            response = self.session.request(method, url, timeout=30, **kwargs)
            Helper.attach_url(response)
            Helper.attach_response(response)
            return response

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)


def list_mobile_cards(api: MobileApiClient, *, all_data: bool | None = None):
    params = None
    if all_data is not None:
        params = {"AllData": str(all_data).lower()}
    return api.get("/cards", headers={"Accept": "*/*"}, params=params)


def list_mobile_cards_v2(api: MobileApiClient, *, all_data: bool | None = None):
    params = None
    if all_data is not None:
        params = {"AllData": str(all_data).lower()}
    return api.get("/cards/v2.0", headers={"Accept": "*/*"}, params=params)


def upload_mobile_attachment(api: MobileApiClient, *, file_path: str):
    headers = dict(api.session.headers)
    headers.pop("Content-Type", None)
    headers["Accept"] = "*/*"

    filename = os.path.basename(file_path)
    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "image/jpeg"

    with open(file_path, "rb") as file:
        return api.session.post(
            api.base_url + "/attachments",
            files={"File": (filename, file, mime)},
            headers=headers,
            allow_redirects=True,
            timeout=30,
        )


def upload_mobile_attachment_v2(
    api: MobileApiClient,
    *,
    file_path: str,
    attribute_id: int,
):
    headers = dict(api.session.headers)
    headers.pop("Content-Type", None)
    headers["Accept"] = "*/*"

    filename = os.path.basename(file_path)
    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "image/jpeg"

    data = {
        "AttributeID": str(attribute_id),
        "Attachments.Index": "0",
        "Attachments[0].IsIgnorePossibleDuplication": "true",
    }

    with open(file_path, "rb") as file:
        return api.session.post(
            api.base_url + "/attachments/v2",
            data=data,
            files={"Attachments[0].File": (filename, file, mime)},
            headers=headers,
            allow_redirects=True,
            timeout=30,
        )


def create_mobile_card(api: MobileApiClient, payload: dict, attachment_id: int):
    variants = []

    first = dict(payload)
    first["Person"] = dict(payload["Person"])
    first["Person"]["Attachments"] = [attachment_id]
    variants.append(first)

    second = dict(payload)
    second["Person"] = dict(payload["Person"])
    second["Person"]["Attachments"] = [{"id": attachment_id}]
    variants.append(second)

    last = None
    for body in variants:
        last = api.post("/cards/V2.0", json=body)
        if last.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
            return last
    return last


def get_mobile_card(api: MobileApiClient, card_id: int):
    return api.get(f"/cards/{int(card_id)}")


def update_mobile_card_v2(api: MobileApiClient, card_id: int, payload: dict):
    return api.put(f"/cards/{int(card_id)}/V2", json=payload)


def merge_mobile_designsettings(api: MobileApiClient, card_id: int, body: dict):
    return api.put(f"/cards/{int(card_id)}/designsettings", json=body)


def get_mobile_designsettings(api: MobileApiClient, card_id: int):
    return api.get(f"/cards/{int(card_id)}/designsettings")


def merge_mobile_card_attributes(api: MobileApiClient, card_id: int, body: list[dict]):
    return api.put(f"/cards/{int(card_id)}/attributes", json=body)


def list_mobile_card_attributes(api: MobileApiClient, card_id: int, **kwargs):
    return api.get(f"/cards/{int(card_id)}/attributes", **kwargs)


def delete_mobile_card(api: MobileApiClient, card_id: int):
    return api.delete(f"/cards/{int(card_id)}")


def delete_mobile_attachment(api: MobileApiClient, attachment_id: int):
    return api.delete(f"/attachments/{int(attachment_id)}")


def delete_mobile_card_with_retry(
    api: MobileApiClient,
    card_id: int,
    *,
    attempts: int = 5,
    step_s: float = 2.0,
):
    last = None
    for _ in range(attempts):
        response = delete_mobile_card(api, card_id)
        last = response

        if response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.GONE):
            return response

        if response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            get_response = get_mobile_card(api, card_id)
            if get_response.status_code in (HTTPStatus.NOT_FOUND, HTTPStatus.GONE):
                return response

        time.sleep(step_s)

    return last


def delete_mobile_attachment_with_retry(
    api: MobileApiClient,
    attachment_id: int,
    *,
    attempts: int = 3,
    step_s: float = 1.0,
):
    last = None
    for _ in range(attempts):
        response = delete_mobile_attachment(api, attachment_id)
        last = response

        if response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.GONE):
            return response

        time.sleep(step_s)

    return last
