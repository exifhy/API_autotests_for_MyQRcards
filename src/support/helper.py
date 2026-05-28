import base64
import json
import time
import urllib.parse

import allure
import requests
from allure_commons.types import AttachmentType
from requests.structures import CaseInsensitiveDict


class Helper:

    def _call(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", 30)
        start = time.time()
        response = requests.request(method, url, **kwargs)
        self.attach_time(start, time.time())
        self.attach_url(response)
        if hasattr(response, "request") and response.request.body:
            self.attach_request(response.request.body)
        self.attach_response(response)
        return response

    @staticmethod
    def attach_response(response) -> None:
        if hasattr(response, "status_code") and hasattr(response, "text"):
            payload = {
                "status_code": response.status_code,
                "reason": getattr(response, "reason", ""),
                "url": getattr(response, "url", ""),
                "body": response.text or "<empty>",
            }
            allure.attach(
                json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
                name="API Response",
                attachment_type=AttachmentType.JSON,
            )
            return

        if isinstance(response, (dict, list)):
            body = json.dumps(response, ensure_ascii=False, indent=2)
        else:
            body = str(response) if response not in (None, "") else "<empty>"
        allure.attach(body.encode("utf-8"), name="API Response", attachment_type=AttachmentType.JSON)

    @staticmethod
    def attach_response_headers(response) -> None:
        headers = dict(response) if isinstance(response, CaseInsensitiveDict) else response
        allure.attach(
            json.dumps(headers, ensure_ascii=False, indent=2).encode("utf-8"),
            name="API Response headers",
            attachment_type=AttachmentType.JSON,
        )

    @staticmethod
    def attach_request(request) -> None:
        if isinstance(request, bytes):
            try:
                request = request.decode("utf-8")
            except UnicodeDecodeError:
                allure.attach(
                    b"<binary / multipart body>",
                    name="API Request body",
                    attachment_type=AttachmentType.TEXT,
                )
                return
        try:
            body = json.dumps(json.loads(request), ensure_ascii=False, indent=2)
        except Exception:
            body = str(request) if request else "<empty>"
        allure.attach(body.encode("utf-8"), name="API Request body", attachment_type=AttachmentType.JSON)

    @staticmethod
    def attach_url(response) -> None:
        if hasattr(response, "request"):
            req = response.request
            payload = {
                "method": getattr(req, "method", "") or "<empty>",
                "url": getattr(req, "url", "") or getattr(response, "url", "") or "<empty>",
            }
            allure.attach(
                json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
                name="Request",
                attachment_type=AttachmentType.JSON,
            )
            return

        payload = {"method": "<unknown>", "url": str(response) if response else "<empty>"}
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
            name="Request",
            attachment_type=AttachmentType.JSON,
        )

    @staticmethod
    def attach_time(start_time: float, end_time: float) -> None:
        ms = (end_time - start_time) * 1000
        allure.attach(
            f"Response time: {ms:.2f} ms",
            name="Response Time",
            attachment_type=AttachmentType.TEXT,
        )

    @staticmethod
    def attach_token(token: str) -> None:
        allure.attach(
            str(token).encode("utf-8"),
            name="Token",
            attachment_type=AttachmentType.TEXT,
        )

    @staticmethod
    def attach_token_expiration_time(expiration_time) -> None:
        allure.attach(
            expiration_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            name="Token Expiration",
            attachment_type=AttachmentType.TEXT,
        )

    @staticmethod
    def response_content(response):
        allure.attach(str(response.request.method), name="Method", attachment_type=AttachmentType.TEXT)
        allure.attach(str(response.status_code), name="Status code", attachment_type=AttachmentType.TEXT)
        if not response.content:
            return "The response body is empty."
        if "application/json" in response.headers.get("Content-Type", ""):
            try:
                return response.json()
            except ValueError as e:
                return f"Invalid JSON response: {e}"
        return "The response body is not JSON."

    @staticmethod
    def basic_token_generation(login: str, password: str) -> str:
        credentials = f"{urllib.parse.quote(login, safe='')}:{urllib.parse.quote(password, safe='')}"
        return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    @staticmethod
    def build_url(base_url: str, params: dict) -> str:
        return f"{base_url}/?{urllib.parse.urlencode(params)}"
