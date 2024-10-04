from config.base_test import BaseTest
from src.enums.params_enums import Params
import allure
import pytest


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthnPasswords(BaseTest):

    @allure.title('Test sets the password for the newly created account.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23454")
    @pytest.mark.skip(reason="Need verification code")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23454)
    @pytest.mark.parametrize('params', Params.params_authn_set_passwords.value)
    def test_post_sets_password_for_new_account(self, params):
        self.api_authn_passwords.post_sets_password_for_new_account(params=params)
