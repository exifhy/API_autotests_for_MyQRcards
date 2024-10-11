import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTasks(BaseTest):

    @pytest.mark.skip(reason='Тест на добавление заявки есть в test_delete_task_by_id')
    @allure.title('Test add task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23230")
    @pytest.mark.test_case_id(23230)
    @pytest.mark.smoke
    def test_add_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        object_model = self.api_es_assets.post_add_object(company_id)
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        model_task = self.api_work_tasks.post_add_task(
            asset_id=object_model.id,
            company_id=company_id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test delete task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23231")
    @pytest.mark.test_case_id(23231)
    @pytest.mark.smoke
    def test_delete_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
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
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test returns a list of tasks available to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23258")
    @pytest.mark.test_case_id(23258)
    @pytest.mark.smoke
    def test_get_list_of_tasks_available_to_user(self):
        self.api_work_tasks.get_list_of_tasks_available_to_user()

    @allure.title('Test returns detailed information on the task by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23264")
    @pytest.mark.test_case_id(23264)
    @pytest.mark.smoke
    def test_get_detailed_info_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
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
        self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test update task by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23265")
    @pytest.mark.test_case_id(23265)
    @pytest.mark.smoke
    def test_put_update_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
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
        task_number, note_task = self.api_work_tasks.put_update_task_by_id(model_task.id)
        model_info_task = self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        assert model_info_task.number == task_number, f'Expected {model_info_task.number}, but got {task_number}'
        assert model_info_task.notes == note_task, f'Expected {model_info_task.notes}, but got {note_task}'
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
