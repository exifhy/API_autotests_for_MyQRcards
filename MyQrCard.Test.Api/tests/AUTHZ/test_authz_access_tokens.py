from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthzAccessTokens(BaseTest):

    @allure.title('Test updates the resource access token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23463")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23463)
    def test_post_updates_resource_access_token(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        model_refresh_token = self.api_authz_refresh_tokens.post_generates_and_returns_refresh_token(
            access_token=model_access_token.access_token
        )
        self.api_authz_access_tokens.post_updates_resource_access_token(
            access_token=model_access_token.access_token,
            refresh_token=model_refresh_token.refresh_token
        )

    @allure.title('Test updates the resource access token (GET refresh token).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25844")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25844)
    @pytest.mark.xfail(reason="Ошибка 401, Закончен период членства в тенанте")
    def test_post_updates_resource_access_token_get_refresh_token(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        model_refresh_token = self.api_authz_refresh_tokens.get_refresh_token_with_default_parameters(
            access_token=model_access_token.access_token
        )
        self.api_authz_access_tokens.post_updates_resource_access_token(
            access_token=model_access_token.access_token,
            refresh_token=model_refresh_token.refresh_token
        )
