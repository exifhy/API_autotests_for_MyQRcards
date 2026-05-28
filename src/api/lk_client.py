from __future__ import annotations

import allure
import requests

from src.support.helper import Helper


class LkApiClient:
    def __init__(self, host: str, token: str, x_application_id: str | None = None):
        self.base_url = host.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
        )
        if x_application_id:
            self.session.headers["X-Application-ID"] = str(x_application_id)

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
