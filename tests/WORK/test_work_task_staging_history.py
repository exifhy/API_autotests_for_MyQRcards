import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTaskStagingHistory(BaseTest):

    @allure.title('Test actual record to the history of the task progress by stage.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23331")
    @pytest.mark.smoke
    @pytest.mark.parametrize('first_stage, second_stage', Params.params_task_staging_first_status.value)
    def test_post_add_task_staging_history_first(self, first_stage, second_stage):
        model_asset = self.api_es_assets.post_add_object()
        self.api_es_asset_districts.add_default_district_to_object(model_asset.id)
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_assetlocations.add_location_to_object(
            asset_id=model_asset.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
        model_task = self.api_work_tasks.post_add_task(asset_id=model_asset.id)
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=first_stage,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=second_stage,
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)

    @allure.title('Test actual record to the history of the task progress by stage.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23331")
    @pytest.mark.smoke
    @pytest.mark.parametrize('first_stage, second_stage, third_stage', Params.params_task_staging_second_status.value)
    def test_post_add_task_staging_history_second(self, first_stage, second_stage, third_stage):
        model_asset = self.api_es_assets.post_add_object()
        self.api_es_asset_districts.add_default_district_to_object(model_asset.id)
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_assetlocations.add_location_to_object(
            asset_id=model_asset.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
        model_task = self.api_work_tasks.post_add_task(asset_id=model_asset.id)
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=first_stage,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=second_stage,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=third_stage,
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)

    @allure.title('Test actual record to the history of the task progress by stage.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23331")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        'first_stage, second_stage, third_stage, fourth_stage',
        Params.params_task_staging_third_status.value
    )
    def test_post_add_task_staging_history_third(self, first_stage, second_stage, third_stage, fourth_stage):
        model_asset = self.api_es_assets.post_add_object()
        self.api_es_asset_districts.add_default_district_to_object(model_asset.id)
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_assetlocations.add_location_to_object(
            asset_id=model_asset.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
        model_task = self.api_work_tasks.post_add_task(asset_id=model_asset.id)
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=first_stage,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=second_stage,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=third_stage,
            task_id=model_task.id
        )
        self.api_work_task_staging_history.post_add_task_staging_history(
            stage_id=fourth_stage,
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)


