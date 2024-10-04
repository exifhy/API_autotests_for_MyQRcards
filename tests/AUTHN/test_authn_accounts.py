from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthnAccounts(BaseTest):

    @allure.title('Test account authentication by email address or username and password via Basic authorisation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23035")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23035)
    def test_account_authentication_by_basic_authorisation(self):
        self.api_authn_accounts.account_authentication_by_basic_authorization()

    @allure.title('Test authentication with invalid TOKEN.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23036")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23036)
    def test_account_authentication_with_invalid_token(self):
        self.api_authn_accounts.account_authentication_with_invalid_token()

    @allure.title('Test request without Authorization header.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23037")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23037)
    def test_request_without_authorization_header(self):
        self.api_authn_accounts.request_without_authorization_header()

    @allure.title('Test account authentication by sso.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23440")
    @pytest.mark.skip(reason="Need Single Sign-On token")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23440)
    def test_post_account_authentication_by_sso(self):
        self.api_authn_accounts.post_account_authentication_by_sso("token")

    @allure.title('Test generating code for authorization via SMS.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23442")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23442)
    def test_post_generating_code_for_authorization_by_sms(self):
        self.api_authn_accounts.post_generating_code_for_authorization_by_sms()

    @allure.title('Test generating code for authorization via SMS with invalid phone number. (00123456456342)')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23445")
    @pytest.mark.regress
    @pytest.mark.test_case_id(234451)
    def test_post_generating_code_for_authorization_by_sms_with_invalid_phone_len(self):
        self.api_authn_accounts.post_generating_code_for_authorization_by_sms_with_invalid_phone_len()

    @allure.title('Test generating code for authorization via SMS with invalid phone number. (abcadsfqwer)')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23445")
    @pytest.mark.regress
    @pytest.mark.test_case_id(234452)
    def test_post_generating_code_for_authorization_by_sms_with_invalid_phone_abc(self):
        self.api_authn_accounts.post_generating_code_for_authorization_by_sms_with_invalid_phone_abc()

    @allure.title('Test SMS code verification.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23443")
    @pytest.mark.skip(reason="Need verification code received by SMS")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23443)
    def test_post_sms_code_verification(self):
        self.api_authn_accounts.post_sms_code_verification(code='code')
