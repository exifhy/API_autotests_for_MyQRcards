from config.base_test import BaseTest
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthMessages(BaseTest):

    @allure.title('Test sends a mail verification e-mail to the specified e-mail address.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23427")
    @pytest.mark.skip(reason='Timeout for re-sending the verification message.')
    @pytest.mark.regress
    @pytest.mark.test_case_id(23427)
    def test_post_message_verify_email(self):
        model = self.api_authn_accounts.account_authentication_by_basic_authorization()
        self.api_auth_messages.post_message_verify_email(
            account_id=model.tenantEntities[0].accountID,
            email=model.tenantEntities[0].email,
            token=model.access_token
        )

    @pytest.mark.skip(reason='Need a registered phone number for the test.')
    @allure.title('Test sends SMS of mail phone number verification to the specified phone number.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23428")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23428)
    def test_post_message_verify_phone(self):
        """Для теста у пользователя должен быть номер телефона."""
        model = self.api_authn_accounts.account_authentication_by_basic_authorization()
        user = self.api_authz_accounts.account_authorization_of_tenant_account(model.access_token)
        self.api_auth_messages.post_message_verify_phone(
            account_id=model.tenantEntities[0].accountID,
            phone=user.profile.mobilePhone,
            token=model.access_token
        )

    @allure.title('Test sends a password change request to the specified e-mail address.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23429")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23429)
    def test_post_message_request_password_change(self):
        model = self.api_authn_accounts.account_authentication_by_basic_authorization()
        self.api_auth_messages.post_message_request_password_change(
            token=model.access_token,
            email=model.tenantEntities[0].email
        )
