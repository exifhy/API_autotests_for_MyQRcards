from __future__ import annotations
import time

from datetime import datetime
from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_contacts_download_csv.endpoints import Endpoints
from services.subscriptions.subscription_contacts_download_csv.models.subscription_contacts_download_csv_model import (
    SubscriptionContactsDownloadCsvModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionContactsDownloadCsvAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @staticmethod
    def build_params(
        *,
        date_from: str,
        date_till: str,
        account_id: int | None = None,
        company_id: int | None = None,
        search_text: str | None = None,
    ) -> dict[str, str]:
        params = {
            "DateFrom": date_from,
            "DateTill": date_till,
        }
        if account_id is not None:
            params["accountID"] = str(account_id)
        if company_id is not None:
            params["companyID"] = str(company_id)
        if search_text:
            params["searchText"] = search_text
        return params

    @staticmethod
    def current_date_till() -> str:
        return datetime.now().strftime("%Y-%m-%dT23:59:59")

    @allure.step("GET /Subscriptions/{sub_id}/contacts/download")
    def download_subscription_contacts_csv(
        self,
        sub_id: int,
        *,
        date_from: str,
        date_till: str,
        account_id: int | None = None,
        company_id: int | None = None,
        search_text: str | None = None,
    ) -> tuple[requests.Response, SubscriptionContactsDownloadCsvModel]:
        params = self.build_params(
            date_from=date_from,
            date_till=date_till,
            account_id=account_id,
            company_id=company_id,
            search_text=search_text,
        )
        headers = Headers.auth_header(bearer_token=get_token())
        headers.pop("Content-Type", None)
        headers["Accept"] = "*/*"

        response = self._call(
            "GET",
            url=self.endpoints.download_subscription_contacts_csv_endpoint.format(sub_id=int(sub_id)),
            headers=headers,
            params=params,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        content_type = response.headers.get("Content-Type") or response.headers.get("content-type") or ""
        body_text = response.content.decode("utf-8-sig", errors="replace")
        return response, SubscriptionContactsDownloadCsvModel(
            content_type=content_type,
            has_bom_utf8=response.content.startswith(b"\xef\xbb\xbf"),
            body_text=body_text,
        )

    @allure.step("GET /Subscriptions/{sub_id}/contacts/download without auth")
    def download_subscription_contacts_csv_without_auth(
        self,
        sub_id: int,
        *,
        date_from: str,
        date_till: str,
        account_id: int | None = None,
        company_id: int | None = None,
        search_text: str | None = None,
    ):
        params = self.build_params(
            date_from=date_from,
            date_till=date_till,
            account_id=account_id,
            company_id=company_id,
            search_text=search_text,
        )
        headers = Headers.without_authorization_field_header()
        headers.pop("Content-Type", None)
        headers["Accept"] = "*/*"

        response = self._call(
            "GET",
            url=self.endpoints.download_subscription_contacts_csv_endpoint.format(sub_id=int(sub_id)),
            headers=headers,
            params=params,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
