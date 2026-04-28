import allure
import pytest
from http import HTTPStatus

from config.config import HOST
from config.headers import Headers
from src.support.helper import Helper


INVALID_TOKENS = [
    pytest.param("", id="empty"),
    pytest.param("garbage_xyz_123", id="garbage"),
    pytest.param(
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmYWtlIn0.fakesig",
        id="malformed_jwt",
    ),
]

PROTECTED_ENDPOINTS = [
    pytest.param(f"{HOST}/Cards", id="GET /Cards"),
    pytest.param(f"{HOST}/Attributes", id="GET /Attributes"),
    pytest.param(f"{HOST}/accounts/contacts", id="GET /accounts/contacts"),
    pytest.param(f"{HOST}/VirtualBackgrounds", id="GET /VirtualBackgrounds"),
]


@allure.epic("Security")
@allure.feature("Auth")
@allure.title("Invalid token → 401/403 on protected endpoints")
@pytest.mark.api
@pytest.mark.ng
class TestInvalidAuthParametrize(Helper):
    @allure.title("Invalid token → 401/403")
    @pytest.mark.parametrize("url", PROTECTED_ENDPOINTS)
    @pytest.mark.parametrize("bad_token", INVALID_TOKENS)
    def test_invalid_token_returns_401_or_403(self, url: str, bad_token: str):
        with allure.step(f"GET {url} with token={bad_token!r}"):
            response = self._call(
                "GET",
                url=url,
                headers=Headers.auth_header(bearer_token=bad_token),
            )

        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403 for token={bad_token!r} on {url}, got {response.status_code}: {response.text}"
        )
