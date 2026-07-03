from config.base_test import BaseTest
import allure
import pytest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthPasswords(BaseTest):

    @allure.title('Test changes the account password.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23411")
    @pytest.mark.skip(reason="Need a generated hash code from an email")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23411)
    @pytest.mark.parametrize('params_password', Params.params_auth_change_passwords.value)
    def test_post_change_password(self, params_password):
        model = self.api_authn_accounts.account_authentication_by_basic_authorization()
        self.api_auth_passwords.post_change_password(
            params=params_password,
            token=model.access_token
        )
        