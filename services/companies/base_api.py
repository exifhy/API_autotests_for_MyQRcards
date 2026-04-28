from __future__ import annotations

import os
from collections.abc import Iterable

import requests

from config.headers import Headers
from src.support.helper import Helper
from src.support.token_utils import get_token


class CompaniesBaseAPI(Helper):
    def _request_headers(self) -> dict:
        token = os.getenv("LK_JWT") or get_token()
        return Headers.auth_header(bearer_token=token)

    def _request(
        self,
        method: str,
        url: str,
        *,
        expected_statuses: Iterable[int],
        json: dict | list | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        response = self._call(
            method,
            url=url,
            headers=headers or self._request_headers(),
            json=json,
            params=params,
        )
        assert response.status_code in tuple(expected_statuses), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        return response
