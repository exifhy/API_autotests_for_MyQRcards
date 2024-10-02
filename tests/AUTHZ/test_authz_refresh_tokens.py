from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthzRefreshTokens(BaseTest):

    @allure.title('Test generates an refresh token and returns it.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23468")
    @pytest.mark.regress
    def test_post_generates_and_returns_refresh_token(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        self.api_authz_refresh_tokens.post_generates_and_returns_refresh_token(
            access_token=model_access_token.access_token
        )

    @allure.title('Test returns the refresh token with default parameters.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23469")
    @pytest.mark.regress
    def test_get_refresh_token_with_default_parameters(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        self.api_authz_refresh_tokens.get_refresh_token_with_default_parameters(
            access_token=model_access_token.access_token
        )
