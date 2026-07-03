import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmGeolocationSettings(BaseTest):

    @allure.title('Test get list geolocation settings.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30252")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30252)
    def test_get_list_geolocation_settings(self):
        self.api_adm_geolocation_settings.get_list_geolocation_settings()

    @allure.title('Test get list geolocation settings without token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30253")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30253)
    def test_get_list_geolocation_settings_without_token(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_without_token()

    @allure.title('Test get list geolocation settings with invalid token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30254")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30254)
    def test_get_list_geolocation_settings_invalid_token(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_invalid_token()

    @allure.title('Test get list geolocation settings with invalid app id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30255")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30255)
    def test_get_list_geolocation_settings_invalid_app_id(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_invalid_app_id()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30256")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30256)
    @pytest.mark.parametrize('content_type', Params.params_content_type_body.value)
    def test_get_list_geolocation_settings_content_type_text_plain(self, content_type, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_with_content_type(content_type)

    @allure.title('Test get list geolocation settings measure response time.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30257")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30257)
    def test_get_list_geolocation_settings_measure_time(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_measure_time()

    @allure.title('Test get list geolocation settings idempotency.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30258")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30258)
    def test_get_list_geolocation_settings_idempotent(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_idempotent()

    @allure.title('Test get list geolocation settings concurrent requests.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30259")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30259)
    def test_get_list_geolocation_settings_concurrent(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_concurrent()

    @allure.title('Test get list geolocation settings verify forbidden access.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30260")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30260)
    def test_get_list_geolocation_settings_forbidden(self):
        self.api_adm_geolocation_settings.get_list_coordinate_accuracy_settings_forbidden()
