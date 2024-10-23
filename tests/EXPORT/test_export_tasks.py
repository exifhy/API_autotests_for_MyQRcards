import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export tasks data")
class TestExportTasks(BaseTest):

    @allure.title('Test returns a list of data available for extended exports.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23209")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23209)
    def test_get_list_data_tasks(self):
        self.api_export_tasks.get_list_data_tasks()

    @allure.title('Test exports the task list into account the specified filters by task id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23232")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23232)
    def test_get_normal_export_task_by_task_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id,
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_export_tasks.get_normal_export_task_by_task_id(model_task.id, model_task.number)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test exports the extended task list into account the specified filters by task id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23233")
    @pytest.mark.xfail(reason="https://dev.azure.com/melston/HubEx/_workitems/edit/23322")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23233)
    def test_get_extended_export_task_by_task_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id,
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_export_tasks.get_extended_export_task_by_task_id(model_task.id, model_task.number)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
