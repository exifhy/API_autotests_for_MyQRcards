import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTaskStagingHistory(BaseTest):

    @allure.title('Test actual record to the history of the task progress by stage.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23331")
    @pytest.mark.xfail(
        reason='Тест не проходит если нет одной из стадий заявки(Исполнитель назначен, В работе, Выполнена, Закрыта).'
    )
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
        try:
            contractor_assigned = self.api_work_tasks.get_list_of_available_stages_to_task_can_transferred(
                task_id=model_task.id,
                stage_name="Исполнитель назначен",
                token=bearer_token
            )
            self.api_work_task_staging_history.post_add_task_staging_history(
                stage_id=contractor_assigned,
                task_id=model_task.id
            )
            in_progress = self.api_work_tasks.get_list_of_available_stages_to_task_can_transferred(
                task_id=model_task.id,
                stage_name="В работе",
                token=bearer_token
            )
            self.api_work_task_staging_history.post_add_task_staging_history(
                stage_id=in_progress,
                task_id=model_task.id
            )
            done = self.api_work_tasks.get_list_of_available_stages_to_task_can_transferred(
                task_id=model_task.id,
                stage_name="Выполнена",
                token=bearer_token
            )
            self.api_work_task_staging_history.post_add_task_staging_history(
                stage_id=done,
                task_id=model_task.id
            )
            closed = self.api_work_tasks.get_list_of_available_stages_to_task_can_transferred(
                task_id=model_task.id,
                stage_name="Закрыта",
                token=bearer_token
            )
            self.api_work_task_staging_history.post_add_task_staging_history(
                stage_id=closed,
                task_id=model_task.id
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test actual record to the history of the task progress by stage (single step from -New-).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23781")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23781)
    def test_post_add_task_staging_history_single_step_from_new(self, bearer_token):
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
        try:
            start_task_stage = self.api_work_task_types.get_route_task_type(task_type_id=task_type_id[0])
            next_task_stage = self.api_tstg_task_stage_links.get_list_task_stage_links_in_tenant(
                task_type_id=task_type_id[0],
                task_stage_from_id=start_task_stage.startTaskStage.id
            )
            self.api_work_task_staging_history.post_add_task_staging_history(
                stage_id=next_task_stage.links[0].toTaskStage.id,
                task_id=model_task.id
            )
            change_task_model = self.api_work_tasks.get_detailed_info_task_by_id(task_id=model_task.id)

            assert change_task_model.taskStage.name == next_task_stage.links[0].toTaskStage.name, \
                f'Expected {next_task_stage.links[0].toTaskStage.name}, but got {change_task_model.taskStage.name}'
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)


