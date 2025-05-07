import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonMeasurementUnits(BaseTest):

    @allure.title('Test get list measurement units.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25694")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25694)
    def test_get_list_measurement_units(self):
        self.api_common_measurement_units.get_list_measurement_units()
