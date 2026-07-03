from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthzTokens(BaseTest):

    @allure.title('Test updates JWT.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23498")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23498)
    def test_post_updates_jwt(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        self.api_authz_tokens.post_update_jwt(
            access_token=model_access_token.access_token
        )
