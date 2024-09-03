from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Registration")
class TestAuthnAccounts(BaseTest):

    @allure.title('Test account authentication by email address or username and password via Basic authorisation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23035")
    @pytest.mark.smoke
    def test_account_authentication_by_basic_authorisation(self):
        self.api_authn_accounts.account_authentication_by_basic_authorisation()

    @allure.title('Test authentication with invalid TOKEN.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23036")
    @pytest.mark.smoke
    def test_account_authentication_with_invalid_token(self):
        self.api_authn_accounts.account_authentication_with_invalid_token()

    @allure.title('Test Request without Authorization header.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23037")
    @pytest.mark.smoke
    def test_request_without_authorization_header(self):
        self.api_authn_accounts.request_without_authorization_header()
