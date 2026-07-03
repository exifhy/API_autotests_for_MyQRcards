import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskTypeDistrict(BaseTest):

    @allure.title('Test changing the binding of task types to district.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25348")
    @pytest.mark.skip(reason="Тест проходит в - test_get_list_districts_task_type")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25348)
    def test_put_update_task_type_district(self):
        model_district = self.api_es_districts.post_add_three_districts()
        model_task_type = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_work_task_type_district.put_update_task_type_district(
            model_task_type[0],
            model_district.districts[0],
            model_district.districts[1],
            model_district.districts[2]
        )
        self.api_es_districts.delete_districts_by_list(
            model_district.districts[0],
            model_district.districts[1],
            model_district.districts[2]
        )
