import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWhWarehouses(BaseTest):

    @allure.title('Test add warehouses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24495")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на создание склада проходит в - test_delete_warehouses_by_list")
    @pytest.mark.test_case_id(24495)
    def test_post_add_warehouses(self):
        self.api_wh_warehouses.post_add_warehouses()

    @allure.title('Test delete warehouses by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24496")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на удаление склада проходит в - test_get_warehouses_by_id")
    @pytest.mark.test_case_id(24496)
    def test_delete_warehouses_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test get warehouse by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24506")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24506)
    def test_get_warehouses_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
