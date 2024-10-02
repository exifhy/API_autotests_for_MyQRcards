from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthzServiceTokens(BaseTest):

    @allure.title('Test generates a new api user access token and returns it.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23488")
    @pytest.mark.regress
    @pytest.mark.skip(reason="The user api token is used for the autotest project. Updating API user token is denied.")
    def test_post_user_api_token_generation(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        self.api_adm_tenant_members.delete_tenant_member_by_id(3)
        model_user = self.api_adm_users.post_add_api_user_in_tenant(
            access_token=model_access_token.access_token
        )
        self.api_authz_service_tokens.post_user_api_token_generation(
            access_token=model_access_token.access_token,
            user_id=model_user.userID
        )

    @allure.title('Test deletes the api user access token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23489")
    @pytest.mark.regress
    @pytest.mark.skip(reason="The user api token is used for the autotest project. Updating API user token is denied.")
    def test_delete_user_api_token(self):
        model_basic_token = self.api_authn_accounts.account_authentication_by_basic_authorization()
        model_access_token = self.api_authz_accounts.account_authorization_of_tenant_account(
            bearer_token=model_basic_token.access_token
        )
        self.api_adm_tenant_members.delete_tenant_member_by_id(3)
        model_user = self.api_adm_users.post_add_api_user_in_tenant(
            access_token=model_access_token.access_token
        )
        self.api_authz_service_tokens.post_user_api_token_generation(
            access_token=model_access_token.access_token,
            user_id=model_user.userID
        )
        self.api_authz_service_tokens.delete_user_api_token(
            access_token=model_access_token.access_token,
            user_id=model_user.userID
        )

