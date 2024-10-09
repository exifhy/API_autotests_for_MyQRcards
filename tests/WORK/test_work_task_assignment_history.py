import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTaskAssignmentHistory(BaseTest):

    @allure.title('Test add  new task to a user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23315")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23315)
    def test_post_add_new_task_to_user(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        object_model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        model_task = self.api_work_tasks.post_add_task(
            asset_id=object_model.id,
            company_id=company_id
        )
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
