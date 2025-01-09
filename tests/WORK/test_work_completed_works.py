import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkCompletedWorks(BaseTest):

    @allure.title('Test creates completed work on task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24342")
    @pytest.mark.skip(reason="Тест на создание проходит в тесте - test_delete_completed_works_by_list")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24342)
    def test_post_add_completed_works(self):
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            self.api_work_completed_works.post_add_completed_works(
                task_id=model_task.id,
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete completed work from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24344")
    @pytest.mark.xfail(reason="Возможно падение https://melston.visualstudio.com/HubEx/_workitems/edit/24002")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24344)
    def test_delete_completed_works_by_list(self):
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            completed_work_id = self.api_work_completed_works.post_add_completed_works(
                task_id=model_task.id,
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
            self.api_work_completed_works.delete_completed_works_by_list(completed_work_id.result[0].id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test update completed work to task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24343")
    @pytest.mark.xfail(reason="Возможно падение https://melston.visualstudio.com/HubEx/_workitems/edit/24002")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24343)
    def test_put_update_completed_works(self):
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            completed_work_id = self.api_work_completed_works.post_add_completed_works(
                task_id=model_task.id,
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
            self.api_work_completed_works.put_update_completed_works(
                completed_work_id=completed_work_id.result[0].id,
                task_id=model_task.id,
                asset_id=object_model.id,
                work_type_id=work_type_id
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
