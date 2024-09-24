from config.base_test import BaseTest
import allure
import pytest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthVerificationCodes(BaseTest):

    @allure.title('Test checks the verification code.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23413")
    @pytest.mark.regress
    @pytest.mark.parametrize('params_codes', Params.params_auth_verification_codes.value)
    def test_post_checks_verification_code(self, params_codes):
        self.api_auth_verifications_codes.post_checks_verification_code(params=params_codes)
