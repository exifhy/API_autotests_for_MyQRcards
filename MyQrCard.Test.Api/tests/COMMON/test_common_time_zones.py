import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonTimezones(BaseTest):

    # @allure.title('Test get list time zones.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25719")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25719)
    # @pytest.mark.skip(reason="Тест дублируется в - test_get_time_zone_info_by_timezone_id.")
    # def test_get_list_time_zones(self):
    #     self.api_common_time_zones.get_list_time_zones()

    @allure.title('Test get time zone info.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25721")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25721)
    def test_get_time_zone_info_by_timezone_id(self):
        model_timezones = self.api_common_time_zones.get_list_time_zones()
        self.api_common_time_zones.get_time_zone_info_by_timezone_id(model_timezones)
