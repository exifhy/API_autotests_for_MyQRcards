from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Registration")
class TestAuthnAccounts(BaseTest):

    @allure.title('Test account authentication by email address or username and password via Basic authorisation.')
    @allure.testcase("TMS-1.1")
    def test_account_authentication_by_basic_authorisation(self):
        self.api_authn_accounts.account_authentication_by_basic_authorisation()

    @allure.title('Test authentication with invalid TOKEN.')
    @allure.testcase("TMS-1.2")
    def test_account_authentication_with_invalid_token(self):
        self.api_authn_accounts.account_authentication_with_invalid_token()

    @allure.title('Test Request without Authorization header.')
    @allure.testcase("TMS-1.3")
    def test_request_without_authorization_header(self):
        self.api_authn_accounts.request_without_authorization_header()
