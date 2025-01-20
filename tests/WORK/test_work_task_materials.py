import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskMaterials(BaseTest):

    @allure.title('Test add task materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24461")
    @pytest.mark.skip(reason="Тест на создание материалов заявки проходит в - ")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24461)
    def test_post_add_task_materials(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventories = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        model_district = self.api_es_districts.post_add_district()
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
        self.api_es_asset_districts.add_districts_to_asset(
            object_model.id,
            model_district.districts[0]
        )
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
            self.api_work_task_materials.post_task_materials(
                model_task.id,
                model_materials.result[0],
                model_wh[0].result[0]
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_districts.delete_district_by_id(model_district.districts[0])
            self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
            self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test delete task materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24462")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24462)
    def test_delete_task_materials(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventories = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        model_district = self.api_es_districts.post_add_district()
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
        self.api_es_asset_districts.add_districts_to_asset(
            object_model.id,
            model_district.districts[0]
        )
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
            model_task_materials = self.api_work_task_materials.post_task_materials(
                model_task.id,
                model_materials.result[0],
                model_wh[0].result[0]
            )
            self.api_work_task_materials.delete_task_materials(model_task.id, model_task_materials.result[0].id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_districts.delete_district_by_id(model_district.districts[0])
            self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
            self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test update task materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24460")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24460)
    def test_put_update_task_materials(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventories = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        model_district = self.api_es_districts.post_add_district()
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
        self.api_es_asset_districts.add_districts_to_asset(
            object_model.id,
            model_district.districts[0]
        )
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
            model_task_materials = self.api_work_task_materials.post_task_materials(
                model_task.id,
                model_materials.result[0],
                model_wh[0].result[0]
            )
            self.api_work_task_materials.put_task_materials(
                model_task.id,
                model_task_materials.result[0].id,
                model_wh[0].result[0]
            )
            self.api_work_task_materials.delete_task_materials(model_task.id, model_task_materials.result[0].id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_districts.delete_district_by_id(model_district.districts[0])
            self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
            self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test update task materials take On.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24463")
    @pytest.mark.skip(
        reason="Тест на взятия необходимых материалов из заявок проходит в - test_put_update_task_materials_take_off"
    )
    @pytest.mark.regress
    @pytest.mark.test_case_id(24463)
    def test_put_update_task_materials_take_on(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventories = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        model_district = self.api_es_districts.post_add_district()
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
        self.api_es_asset_districts.add_districts_to_asset(
            object_model.id,
            model_district.districts[0]
        )
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
            model_task_materials = self.api_work_task_materials.post_task_materials(
                model_task.id,
                model_materials.result[0],
                model_wh[0].result[0]
            )
            self.api_work_task_materials.put_task_materials_take_on(
                model_task.id,
                model_task_materials.result[0].id
            )
            self.api_work_task_materials.delete_task_materials(model_task.id, model_task_materials.result[0].id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_districts.delete_district_by_id(model_district.districts[0])
            self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
            self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test update task materials take Off.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24464")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24464)
    def test_put_update_task_materials_take_off(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventories = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        model_district = self.api_es_districts.post_add_district()
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
        self.api_es_asset_districts.add_districts_to_asset(
            object_model.id,
            model_district.districts[0]
        )
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
            model_task_materials = self.api_work_task_materials.post_task_materials(
                model_task.id,
                model_materials.result[0],
                model_wh[0].result[0]
            )
            self.api_work_task_materials.put_task_materials_take_on(
                model_task.id,
                model_task_materials.result[0].id
            )
            self.api_work_task_materials.put_task_materials_take_off(
                model_task.id,
                model_task_materials.result[0].id
            )
            self.api_work_task_materials.delete_task_materials(model_task.id, model_task_materials.result[0].id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_es_districts.delete_district_by_id(model_district.districts[0])
            self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
            self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
