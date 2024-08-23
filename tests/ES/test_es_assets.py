import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params
import time


@allure.epic("Administration")
@allure.feature("Actions with the object")
class TestEsAssets(BaseTest):

    @allure.title('Test returns the directory of objects available to the user.')
    @allure.testcase("TMS-3.1")
    @pytest.mark.parametrize('param', Params.params_assets_list.value)
    def test_get_directory_of_objects_available_to_user(self, param):
        self.api_es_assets.get_directory_of_objects_available_to_user(param)

    @allure.title('Test object creation.')
    @allure.testcase("TMS-3.2")
    def test_post_add_object(self):
        self.api_es_assets.post_add_object()

    @allure.title('Test marks the object as remote.')
    @allure.testcase("TMS-3.3")
    def test_delete_object_by_id(self):
        model = self.api_es_assets.post_add_object()
        time.sleep(2)
        self.api_es_assets.delete_object_by_id(model.id)

    @allure.title('Test detailed information on the object by id.')
    @allure.testcase("TMS-3.4")
    def test_get_detailed_information_on_object_by_id(self):
        model = self.api_es_assets.post_add_object()
        time.sleep(3)
        self.api_es_assets.get_detailed_information_on_object_by_id(model.id)
