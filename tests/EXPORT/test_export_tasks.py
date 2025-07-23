import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export tasks data")
class TestExportTasks(BaseTest):

    @allure.title('Test get list of tasks extended includes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23209")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23209)
    def test_get_list_of_tasks_extended_includes(self):
        self.api_export_tasks.get_list_of_tasks_extended_includes()

    @allure.title('Test get exports an empty template for importing task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26780")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26780)
    def test_get_export_empty_template_for_importing_task(self):
        self.api_export_tasks.get_export_empty_template_for_importing_task()

    @allure.title('Test exports the task list into account the specified filters by task number.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23232")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23232)
    def test_get_normal_export_task_by_task_number(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        user_stuff = self.api_adm_users.post_add_user_staff()
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
            asset_type_id=asset_type_id,
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
        model_contact = self.api_common_contacts.post_add_contacts()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id,
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, model_contact.contact[0])
        self.api_work_task_assignment_history.post_add_new_task_to_user(user_stuff.userID, model_task.id)
        model_contact_result = self.api_common_contacts.get_data_contact_by_id(model_contact.contact[0])
        model_task_result = self.api_work_tasks.get_task_by_id(model_task.id)
        try:
            self.api_export_tasks.get_normal_export_task_by_task_number(
                model_task_result, model_contact_result
            )
        finally:
            self.api_work_tasks.delete_task_by_list(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_contact_by_id(model_contact.contact[0])
            self.api_adm_users.delete_user_by_id(user_stuff.userID)

    @allure.title('Test exports the task list into account the specified filters by task number, V2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26784")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26784)
    def test_get_normal_export_task_by_task_number_v2(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        user_stuff = self.api_adm_users.post_add_user_staff()
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
            asset_type_id=asset_type_id,
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
        model_contact = self.api_common_contacts.post_add_contacts()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id,
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, model_contact.contact[0])
        self.api_work_task_assignment_history.post_add_new_task_to_user(user_stuff.userID, model_task.id)
        model_contact_result = self.api_common_contacts.get_data_contact_by_id(model_contact.contact[0])
        model_task_result = self.api_work_tasks.get_task_by_id(model_task.id)
        try:
            self.api_export_tasks.get_normal_export_task_by_task_number_v2(
                model_task_result, model_contact_result
            )
        finally:
            self.api_work_tasks.delete_task_by_list(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_contact_by_id(model_contact.contact[0])
            self.api_adm_users.delete_user_by_id(user_stuff.userID)

    @allure.title('Test exports the extended task list into account the specified filters by task number.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23233")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23233)
    def test_get_all_extended_export_task_by_task_number(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        user_stuff = self.api_adm_users.post_add_user_staff()
        responsible_user_stuff = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object_with_responsible(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id,
            responsible_id=responsible_user_stuff.userID
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
        model_empty_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        model_contact = self.api_common_contacts.post_add_contacts()
        model_task = self.api_work_tasks.post_add_task_with_parent_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id,
            parent_id=model_empty_task.id
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, model_contact.contact[0])
        self.api_work_task_assignment_history.post_add_new_task_to_user(user_stuff.userID, model_task.id)
        model_contact_result = self.api_common_contacts.get_data_contact_by_id(model_contact.contact[0])
        model_task_result = self.api_work_tasks.get_task_by_id(model_task.id)
        model_asset_result = self.api_es_assets.get_detailed_information_on_object_by_id(object_model.id)
        model_district = self.api_es_assets.get_list_districts_for_asset(object_model.id)
        try:
            self.api_export_tasks.get_extended_export_task_by_task_number(
                model_task_result, model_contact_result, model_asset_result, model_district
            )
        finally:
            self.api_work_tasks.delete_task_by_list(model_task.id, model_empty_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_contact_by_id(model_contact.contact[0])
            self.api_adm_users.delete_users_by_list(user_stuff.userID, responsible_user_stuff.userID)

    @allure.title('Test exports the extended task list into account the specified filters by task number, V2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26778")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26778)
    def test_get_all_extended_export_task_by_task_number_v2(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        user_stuff = self.api_adm_users.post_add_user_staff()
        responsible_user_stuff = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object_with_responsible(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id,
            responsible_id=responsible_user_stuff.userID
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
        model_empty_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        model_contact = self.api_common_contacts.post_add_contacts()
        model_task = self.api_work_tasks.post_add_task_with_parent_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id,
            parent_id=model_empty_task.id
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, model_contact.contact[0])
        self.api_work_task_assignment_history.post_add_new_task_to_user(user_stuff.userID, model_task.id)
        model_contact_result = self.api_common_contacts.get_data_contact_by_id(model_contact.contact[0])
        model_task_result = self.api_work_tasks.get_task_by_id(model_task.id)
        model_asset_result = self.api_es_assets.get_detailed_information_on_object_by_id(object_model.id)
        model_district = self.api_es_assets.get_list_districts_for_asset(object_model.id)
        try:
            self.api_export_tasks.get_extended_export_task_by_task_number_v2(
                model_task_result, model_contact_result, model_asset_result, model_district
            )
        finally:
            self.api_work_tasks.delete_task_by_list(model_task.id, model_empty_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_contact_by_id(model_contact.contact[0])
            self.api_adm_users.delete_users_by_list(user_stuff.userID, responsible_user_stuff.userID)
