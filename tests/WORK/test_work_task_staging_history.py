import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskStagingHistory(BaseTest):

    @allure.title('Test actual record to the history of the task progress by stage.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23331")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23331)
    def test_post_add_task_staging_history(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_districts.add_default_district_to_object(model_asset.id)
        self.api_es_assetlocations.add_location_to_object(
            asset_id=model_asset.id,
            location_id=location_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=model_asset.id,
            work_type_id=work_type_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=model_asset.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        model_route = self.api_work_task_types.get_route_task_type(task_type_id=task_type_id[0])
        self.api_tstg_task_stage_links.get_list_task_stage_path_switch_from_start_to_finish(
            task_type_id=task_type_id[0],
            start_task_stage_id=model_route.startTaskStage.id,
            finish_task_stage_id=model_route.finishTaskStage.id,
            task_id=model_task.id
        )
        self.api_work_tasks.put_task_completed(model_task.id, bearer_token)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    # @allure.title('Test mass movement of task by stages.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23332")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(23332)
    # @pytest.mark.skip(reason="Ручка отключена, функционал в POST WORK/TaskStagingHistory/batch")
    # def test_post_multiple_add_task_staging_history(self, bearer_token):
    #     company_id = self.api_es_companies.post_add_our_company()
    #     location_id = self.api_es_locations.post_add_location()
    #     self.api_es_company_locations.post_add_company_locations(
    #         company_id=company_id,
    #         location_id=location_id
    #     )
    #     asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
    #     asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
    #     work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
    #     model_asset = self.api_es_assets.post_add_object(
    #         company_id=company_id,
    #         asset_class_id=asset_class_id,
    #         asset_type_id=asset_type_id
    #     )
    #     self.api_es_asset_districts.add_default_district_to_object(model_asset.id)
    #     self.api_es_assetlocations.add_location_to_object(
    #         asset_id=model_asset.id,
    #         location_id=location_id
    #     )
    #     self.api_es_asset_work_types.post_add_work_type_to_asset(
    #         asset_id=model_asset.id,
    #         work_type_id=work_type_id
    #     )
    #     self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
    #     criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
    #     task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
    #     model_task1 = self.api_work_tasks.post_add_task(
    #         criticality_id=criticality_id,
    #         task_type_id=task_type_id[0],
    #         asset_id=model_asset.id,
    #         work_type_id=work_type_id,
    #         company_id=company_id
    #     )
    #     model_task2 = self.api_work_tasks.post_add_task(
    #         criticality_id=criticality_id,
    #         task_type_id=task_type_id[0],
    #         asset_id=model_asset.id,
    #         work_type_id=work_type_id,
    #         company_id=company_id
    #     )
    #     model_task3 = self.api_work_tasks.post_add_task(
    #         criticality_id=criticality_id,
    #         task_type_id=task_type_id[0],
    #         asset_id=model_asset.id,
    #         work_type_id=work_type_id,
    #         company_id=company_id
    #     )
    #     model_route = self.api_work_task_types.get_route_task_type(task_type_id=task_type_id[0])
    #     self.api_work_task_staging_history.post_multiple_add_task_staging_history(
    #         [model_route.finishTaskStage.id, model_route.finishTaskStage.id, model_route.finishTaskStage.id],
    #         [model_task1.id, model_task2.id, model_task3.id]
    #     )
    #     self.api_work_tasks.put_task_completed(model_task1.id, bearer_token)
    #     self.api_work_tasks.put_task_completed(model_task2.id, bearer_token)
    #     self.api_work_tasks.put_task_completed(model_task3.id, bearer_token)
    #     self.api_work_tasks.delete_task_by_list(model_task1.id, model_task2.id, model_task3.id)
    #     self.api_es_assets.delete_object_by_id(model_asset.id)
    #     self.api_es_companies.delete_company_by_id(company_id)
    #     self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test mass movement of task by stages. Batch.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26215")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26215)
    def test_post_multiple_add_task_staging_history_batch(self, bearer_token):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_districts.add_default_district_to_object(model_asset.id)
        self.api_es_assetlocations.add_location_to_object(
            asset_id=model_asset.id,
            location_id=location_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=model_asset.id,
            work_type_id=work_type_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task1 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=model_asset.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task2 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=model_asset.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task3 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=model_asset.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            model_route = self.api_work_tasks.get_task_stages_next(
                model_task1.id, model_task2.id, model_task3.id
            )
            self.api_work_task_staging_history.post_multiple_add_task_staging_history_batch(
                [model_route.results[0].nextStages[0].nextStage.id],
                [[model_task1.id, model_task2.id, model_task3.id]]
            )
        finally:
            self.api_work_tasks.put_task_completed(model_task1.id, bearer_token)
            self.api_work_tasks.put_task_completed(model_task2.id, bearer_token)
            self.api_work_tasks.put_task_completed(model_task3.id, bearer_token)
            self.api_work_tasks.delete_task_by_list(model_task1.id, model_task2.id, model_task3.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test mass movement of 500 tasks by stages. Batch.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26614")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26614)
    def test_post_multiple_add_500_tasks_staging_history_batch(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        list_tasks = self.api_work_tasks.post_create_multiple_tasks(
            task_type_id[0], 500
        )
        try:
            model_route = self.api_work_tasks.get_task_stages_next_by_list(list_tasks)
            self.api_work_task_staging_history.post_multiple_add_task_staging_history_batch(
                [model_route.results[0].nextStages[0].nextStage.id],
                [list_tasks]
            )
            self.api_work_tasks.check_movement_at_the_task_stage(
                list_tasks, model_route.results[0].nextStages[0].nextStage.id, 300
            )
        finally:
            self.api_work_tasks.delete_mass_tasks_by_list(list_tasks)
