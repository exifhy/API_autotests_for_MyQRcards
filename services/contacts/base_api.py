from __future__ import annotations

from config.headers import Headers
from src.support.token_utils import get_token


class ContactsBaseAPI:
    @staticmethod
    def build_headers(*, app_id: str | None = None, accept: str = "application/json") -> dict:
        headers = Headers.auth_header(bearer_token=get_token(), app_id=app_id)
        headers["Accept"] = accept
        if app_id:
            # Keep both header spellings because legacy contact endpoints have been
            # seen accepting the typo variant in older helper code.
            headers["X-Aplication-ID"] = str(app_id)
        return headers
