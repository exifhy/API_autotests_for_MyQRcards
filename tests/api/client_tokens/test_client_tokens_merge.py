import time
import uuid
from http import HTTPStatus

import allure
import pytest

from services.client_tokens.client_tokens_get.api_client_tokens_get import ClientTokensGetAPI
from services.client_tokens.client_tokens_merge.api_client_tokens_merge import ClientTokensMergeAPI


@allure.epic("API")
@allure.feature("ClientTokens")
@pytest.mark.api
@allure.description(
    """
    PUT /clientTokens
    GET /clientTokens
    """
)
class TestClientTokensMerge:
    @allure.title("PUT /clientTokens updates push token and GET returns updated value")
    def test_client_tokens_merge_202(self):
        before = ClientTokensGetAPI().get_client_tokens()
        # 204 = no token registered yet — generate a new clientID
        client_id = before.clientID or str(uuid.uuid4())
        original_push_token = before.pushToken
        new_push_token = f"autotest_push_{int(time.time())}"

        try:
            response, payload = ClientTokensMergeAPI().merge_client_tokens(
                client_id=client_id,
                push_token=new_push_token,
            )
            assert response.status_code == HTTPStatus.ACCEPTED

            after = ClientTokensGetAPI().get_client_tokens()
            assert after.clientID == client_id
            assert after.pushToken == payload["pushToken"]
        finally:
            if original_push_token:
                ClientTokensMergeAPI().merge_client_tokens(
                    client_id=client_id,
                    push_token=original_push_token,
                )

    @allure.title("PUT /clientTokens without auth")
    @pytest.mark.ng
    def test_client_tokens_merge_401_without_auth(self):
        current = ClientTokensGetAPI().get_client_tokens()
        client_id = current.clientID or str(uuid.uuid4())

        response, _ = ClientTokensMergeAPI().merge_client_tokens_without_auth(
            client_id=client_id,
            push_token=f"autotest_push_ng_{int(time.time())}",
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
