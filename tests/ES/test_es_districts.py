import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params
import time


@allure.epic("Administration")
@allure.feature("Actions with the districts")
class TestEsDistricts(BaseTest):

    @pytest.mark.skip(reason='District is created in test - test_delete_district_by_id.')
    @allure.title('Test add district.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23087")
    def test_post_add_district(self):
        self.api_es_districts.post_add_district()

    @allure.title('Test marks the district as remote.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23088")
    def test_delete_district_by_id(self):
        district_id = self.api_es_districts.post_add_district()
        self.api_es_districts.delete_district_by_id(district_id=district_id.districts[0])

