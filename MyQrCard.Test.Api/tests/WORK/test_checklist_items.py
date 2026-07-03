import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkChecklistItems(BaseTest):

    # @allure.title('Test add checklist items.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23912")
    # @pytest.mark.skip(reason="Тест на создание элемента чек-листа проходит в - test_delete_checklist_items")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(23912)
    # def test_post_add_checklist_items(self):
    #     model_checklist = self.api_work_checklists.post_add_checklists()
    #     self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])

    @allure.title('Test delete checklist items.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23914")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23914)
    def test_delete_checklist_items(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        model_checklist_items = self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        self.api_work_checklist_items.delete_checklist_items(
            checklist_id=model_checklist.result[0],
            checklist_item_id=model_checklist_items.result[0].checkListItemID
        )
        self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
