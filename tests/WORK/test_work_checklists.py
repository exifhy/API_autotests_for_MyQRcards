import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkChecklists(BaseTest):

    @allure.title('Test add checklists.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23908")
    @pytest.mark.skip(reason="Тест на создание чек-листа проходит в - test_delete_checklist_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23908)
    def test_post_add_checklists(self):
        self.api_work_checklists.post_add_checklists()

    @allure.title('Test delete checklist by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23910")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23910)
    def test_delete_checklist_by_id(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test get checklist by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23942")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23942)
    def test_get_checklist_by_id(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        try:
            self.api_work_checklists.get_checklist_by_id(model_checklist.result[0])
        finally:
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
