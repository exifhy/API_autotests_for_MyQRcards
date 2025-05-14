import time
from src.enums.params_enums import Params
import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTasks(BaseTest):

    @allure.title('Test get task assignments history.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24672")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24672)
    def test_get_list_task_assignments(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_user = self.api_adm_users.post_add_user_staff()
        model_assignment = self.api_work_task_assignment_history.post_add_new_task_to_user(
            user_id=model_user.userID,
            task_id=model_task.id
        )
        self.api_work_tasks.get_list_task_assignments(model_task.id, model_assignment)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list task attachments.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24677")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24677)
    def test_get_list_task_attachments(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_attach = self.api_work_task_attachments.post_upload_attachment_and_bind_to_task_data_from_form(
            model_task.id
        )
        self.api_work_tasks.get_list_task_attachments(
            model_task.id,
            model_attach
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get task attachment by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24691")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24691)
    def test_get_task_attachment_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_attach = self.api_work_task_attachments.post_upload_attachment_and_bind_to_task_data_from_form(
            model_task.id
        )
        self.api_work_tasks.get_task_attachment_by_id(
            model_task.id,
            model_attach
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get temporary link for downloading task attachment.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24698")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24698)
    def test_get_temporary_link_for_downloading_task_attachment(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_attach = self.api_work_task_attachments.post_upload_attachment_and_bind_to_task_data_from_form(
            model_task.id
        )
        self.api_work_tasks.get_downloading_attachment_file_from_task(
            model_task.id,
            model_attach
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get temporary link for downloading task attachment. No Redirect.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24699")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24699)
    def test_get_link_task_attachment_no_redirect(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_attach = self.api_work_task_attachments.post_upload_attachment_and_bind_to_task_data_from_form(
            model_task.id
        )
        self.api_work_tasks.get_link_task_attachment_no_redirect(
            model_task.id,
            model_attach
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get task attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24700")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24700)
    def test_get_task_attributes(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_task_str()
        model_attribute = self.api_common_attributes.get_attribute_by_id(attribute_id.values[0])
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.get_task_attributes(
            model_task.id,
            attribute_id.values[0],
            model_attribute
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list of logging supported partitions (Tab) and sections of these partitions (Sections).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24704")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24704)
    def test_get_list_task_change_types(self):
        self.api_work_tasks.get_list_task_change_types()

    @allure.title('Test get list changes history of the task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24727")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24727)
    def test_get_list_task_changes_history(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.get_list_task_changes_history(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list of checklists in the task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24731")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24731)
    def test_get_list_task_checklists(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.post_add_checklists_to_task_by_id(model_task.id, model_checklist.result[0])
        self.api_work_tasks.get_list_task_checklists(model_task.id, model_checklist.result[0])
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test adds checklists to the task by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24734")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24734)
    def test_post_add_checklists_to_task_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            self.api_work_tasks.post_add_checklists_to_task_by_list(model_task.id, model_checklist.result[0])
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test adds checklists to the task by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24728")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24728)
    def test_post_add_checklists_to_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            self.api_work_tasks.post_add_checklists_to_task_by_id(model_task.id, model_checklist.result[0])
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete checklists from task by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24735")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24735)
    def test_delete_checklists_from_task_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_id(
                model_task.id,
                model_checklist.result[0]
            )
            self.api_work_tasks.delete_checklists_from_task_by_list(
                model_task.id,
                str(model_task_checklist.result[0].id)
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete checklists from task by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24739")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24739)
    def test_delete_checklist_from_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
                model_task.id,
                model_checklist.result[0]
            )
            self.api_work_tasks.delete_checklist_from_task_by_id(model_task.id, model_task_checklist.result[0].id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test upload file to server and bind to task checklist, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24742")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24742)
    def test_post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
            model_task.id,
            model_checklist.result[0]
        )
        model_task_checklist_result = self.api_work_tasks.get_results_task_checklists_v2(
            model_task.id,
            model_task_checklist.result[0].id,
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(
            task_id=model_task.id,
            task_checklist_result_id=next(iter(model_task_checklist_result.root)),
            task_checklist_id=model_task_checklist.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get results of checklists in the task v2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24743")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24743)
    def test_get_results_task_checklists_v2(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
                model_task.id,
                model_checklist.result[0]
            )
            self.api_work_tasks.get_results_task_checklists_v2(
                model_task.id,
                model_task_checklist.result[0].id,
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test upload file to server and bind to attribute task completed work, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24854")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24854)
    def test_post_upload_attachment_to_server_bind_attribute_task_completed_work_data_from_form(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_complete_work()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        try:
            model_attachment = self.api_work_tasks.post_upload_attachment_to_server_bind_attribute_task_completed_work_data_from_form(
                task_id=model_task.id,
                completed_work_id=model_completed_work.result[0].id,
                attribute_id=attribute_id
            )
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachments[0])
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attachments from items of checklists in the task by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24855")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24855)
    def test_get_list_attachments_task_checklists_items_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
            model_task.id,
            model_checklist.result[0]
        )
        model_task_checklist_result = self.api_work_tasks.get_results_task_checklists_v2(
            model_task.id,
            model_task_checklist.result[0].id,
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(
            task_id=model_task.id,
            task_checklist_result_id=next(iter(model_task_checklist_result.root)),
            task_checklist_id=model_task_checklist.result[0].id
        )
        try:
            self.api_work_tasks.get_list_attachments_task_checklists_items_id(
                task_id=model_task.id,
                task_checklist_result_id=next(iter(model_task_checklist_result.root)),
                task_checklist_id=model_task_checklist.result[0].id
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attachments from items of checklists in the task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24856")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24856)
    def test_get_list_attachments_task_checklists_items(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
            model_task.id,
            model_checklist.result[0]
        )
        model_task_checklist_result = self.api_work_tasks.get_results_task_checklists_v2(
            model_task.id,
            model_task_checklist.result[0].id,
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(
            task_id=model_task.id,
            task_checklist_result_id=next(iter(model_task_checklist_result.root)),
            task_checklist_id=model_task_checklist.result[0].id
        )
        try:
            self.api_work_tasks.get_list_attachments_task_checklists_items(
                task_id=model_task.id,
                task_checklist_id=model_task_checklist.result[0].id
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get data attachment from items of checklists in the task by attach ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24858")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24858)
    def test_get_attachment_task_checklists_items_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
            model_task.id,
            model_checklist.result[0]
        )
        model_task_checklist_result = self.api_work_tasks.get_results_task_checklists_v2(
            model_task.id,
            model_task_checklist.result[0].id,
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(
            task_id=model_task.id,
            task_checklist_result_id=next(iter(model_task_checklist_result.root)),
            task_checklist_id=model_task_checklist.result[0].id
        )
        try:
            self.api_work_tasks.get_attachment_task_checklists_items_by_id(
                task_id=model_task.id,
                task_checklist_result_id=next(iter(model_task_checklist_result.root)),
                task_checklist_id=model_task_checklist.result[0].id,
                attachment_id=model_attach.attachments[0]
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete results checklist from task by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24859")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24859)
    def test_delete_results_checklist_from_task_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
            model_task.id,
            model_checklist.result[0]
        )
        model_task_checklist_result = self.api_work_tasks.get_results_task_checklists_v2(
            model_task.id,
            model_task_checklist.result[0].id,
        )
        try:
            self.api_work_tasks.delete_results_checklist_from_task_by_list(
                model_task.id,
                model_task_checklist.result[0].id,
                int(next(iter(model_task_checklist_result.root)))
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test update results items of checklists in the task v2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24860")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24860)
    def test_put_update_results_task_checklists_items_v2(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_checklist = self.api_work_checklists.post_add_checklists()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_checklist()
        self.api_work_checklist_items.post_add_checklist_items_foto(
            model_checklist.result[0],
            attribute_id
        )
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task_checklist = self.api_work_tasks.post_add_checklists_to_task_by_list(
            model_task.id,
            model_checklist.result[0]
        )
        model_task_checklist_result = self.api_work_tasks.get_results_task_checklists_v2(
            model_task.id,
            model_task_checklist.result[0].id
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(
            task_id=model_task.id,
            task_checklist_result_id=next(iter(model_task_checklist_result.root)),
            task_checklist_id=model_task_checklist.result[0].id
        )
        try:
            self.api_work_tasks.put_update_results_task_checklists_items_v2(
                model_task.id,
                model_task_checklist.result[0].id,
                next(iter(model_task_checklist_result.root)),
                model_attach.attachments[0],
                True,
                "Attachment"
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attachments bind to attribute task completed work by attribute ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24861")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24861)
    def test_get_list_attachments_from_attribute_task_completed_work_by_attribute_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_complete_work()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        model_attachment = self.api_work_tasks.post_upload_attachment_to_server_bind_attribute_task_completed_work_data_from_form(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            attribute_id=attribute_id
        )
        self.api_work_tasks.get_list_attachments_from_attribute_task_completed_work_by_attribute_id(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            attribute_id=attribute_id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attachment.attachments[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attachments bind to attribute task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24862")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24862)
    def test_get_list_attachments_from_attribute_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.get_list_attributes_return_id_attribute_attachment_for_complete_work()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        model_attachment = self.api_work_tasks.post_upload_attachment_to_server_bind_attribute_task_completed_work_data_from_form(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            attribute_id=attribute_id
        )
        self.api_work_tasks.get_list_attachments_from_attribute_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attachment.attachments[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attributes task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24870")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24870)
    def test_get_list_attributes_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.get_list_attributes_task_completed_work(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attributes task completed work by completed work ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24874")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24874)
    def test_get_list_attributes_task_completed_work_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.get_list_attributes_task_completed_work_by_id(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete attributes task completed work by list and completed work ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24893")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24893)
    def test_delete_attributes_task_completed_work_id_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.delete_attributes_task_completed_work_id_by_list(
            model_task.id,
            model_completed_work.result[0].id,
            attribute_id.values[0]
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete attributes task completed work by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24902")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24902)
    def test_delete_attributes_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.delete_attributes_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            attribute_id.values[0]
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete attribute task completed work by attribute ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24904")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24904)
    def test_delete_attribute_task_completed_work_by_attribute_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.delete_attribute_task_completed_work_by_attribute_id(
            model_task.id,
            model_completed_work.result[0].id,
            attribute_id.values[0]
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test update attributes task completed work by completed work ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24894")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24894)
    def test_put_update_attributes_task_completed_work_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.put_update_attributes_task_completed_work_by_id(
            model_task.id,
            model_completed_work.result[0].id,
            attribute_id.values[0]
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test update attributes task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24897")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24897)
    def test_put_update_attributes_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_complete_work_string()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.put_update_attributes_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            attribute_id.values[0]
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24905")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24905)
    def test_get_list_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.get_list_task_completed_work(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get task completed work by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24909")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24909)
    def test_get_task_completed_work_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.get_task_completed_work_id(model_task.id, model_completed_work.result[0].id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attachments task completed work by complected work ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24921")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24921)
    def test_get_list_attachments_task_completed_work_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_completed_work_attachments.post_upload_and_bind_to_completed_work_data_from_form(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.get_list_attachments_task_completed_work_id(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list attachments task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24923")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24923)
    def test_get_list_attachments_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_completed_work_attachments.post_upload_and_bind_to_completed_work_data_from_form(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.get_list_attachments_task_completed_work(
            model_task.id,
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test download attachment from task completed work by ID. No redirect.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24926")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24926)
    def test_get_download_attachment_from_task_completed_work_by_id_no_redirect(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        attachment_id = self.api_work_completed_work_attachments.post_upload_and_bind_to_completed_work_data_from_form(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.get_download_attachment_from_task_completed_work_by_id_no_redirect(
            model_task.id,
            model_completed_work.result[0].id,
            attachment_id.attachmentID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test download attachment from task completed work by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24927")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24927)
    def test_get_download_attachment_from_task_completed_work_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        attachment_id = self.api_work_completed_work_attachments.post_upload_and_bind_to_completed_work_data_from_form(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.get_download_attachment_from_task_completed_work_by_id(
            model_task.id,
            model_completed_work.result[0].id,
            attachment_id.attachmentID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test add technicians to task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24936")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24936)
    def test_post_add_technicians_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test add materials to task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24948")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24948)
    def test_post_add_materials_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventory_id = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.user.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_wh_materials.delete_materials_by_list(materials_data.id)
        self.api_wh_warehouses.delete_warehouses_by_list(wh_data.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test update materials to task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24961")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24961)
    def test_put_update_materials_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventory_id = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.user.id
        )
        self.api_work_tasks.put_update_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_wh_materials.delete_materials_by_list(materials_data.id)
        self.api_wh_warehouses.delete_warehouses_by_list(wh_data.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list materials task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24951")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24951)
    def test_get_list_materials_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventory_id = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.user.id
        )
        self.api_work_tasks.get_list_materials_task_completed_work(model_task.id, model_completed_work.result[0].id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_wh_materials.delete_materials_by_list(materials_data.id)
        self.api_wh_warehouses.delete_warehouses_by_list(wh_data.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete materials task completed work by completed work Id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24953")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24953)
    def test_delete_materials_task_completed_work_by_completed_work_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventory_id = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.user.id
        )
        self.api_work_tasks.delete_materials_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            materials_data.id,
            wh_data.id,
            model_inventory_id.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_wh_materials.delete_materials_by_list(materials_data.id)
        self.api_wh_warehouses.delete_warehouses_by_list(wh_data.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete materials task completed works.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24965")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24965)
    def test_delete_materials_task_completed_works(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventory_id = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.user.id
        )
        self.api_work_tasks.delete_materials_task_completed_works(
            model_task.id,
            model_completed_work.result[0].id,
            materials_data.id,
            wh_data.id,
            model_inventory_id.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_wh_materials.delete_materials_by_list(materials_data.id)
        self.api_wh_warehouses.delete_warehouses_by_list(wh_data.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test upload file to server and bind to report task completed work, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24969")
    @pytest.mark.xfail(reason="Ручка загрузки из формы подписи в акт выполненной работы работает через раз (400).")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24969)
    def test_post_upload_attachment_to_server_bind_report_task_completed_work_data_from_form(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        attach_id = self.api_work_tasks.post_upload_attachment_to_server_bind_report_task_completed_work_data_from_form(
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(attach_id.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test upload file to server and bind to report task completed work, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24980")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24980)
    def test_post_upload_attachment_to_server_bind_report_task_completed_work_data_from_body(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        time.sleep(2)
        attach_id = self.api_work_tasks.post_upload_signature_to_report_task_completed_works_data_from_body(
            task_id=model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(attach_id.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get signature from report task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24972")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24972)
    def test_get_signature_report_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        time.sleep(2)
        attach_id = self.api_work_tasks.post_upload_signature_to_report_task_completed_works_data_from_body(
            task_id=model_task.id
        )
        self.api_work_tasks.get_signature_report_task_completed_work(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(attach_id.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete signature report task completed works.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24971")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24971)
    def test_delete_signature_report_task_completed_works(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        time.sleep(2)
        attach_id = self.api_work_tasks.post_upload_signature_to_report_task_completed_works_data_from_body(
            task_id=model_task.id
        )
        self.api_work_tasks.delete_signature_report_task_completed_works(
            task_id=model_task.id,
            attachment_id=attach_id.attachmentID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(attach_id.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test add uploaded signature to report task completed works V2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24979")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24979)
    def test_post_add_uploaded_signature_to_report_task_completed_works_v2(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        model_attach = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        self.api_work_tasks.post_add_uploaded_signature_to_report_task_completed_works_v2(
            model_task.id,
            model_attach.attachmentID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test add uploaded signature to report task completed works.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24975")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24975)
    def test_post_add_uploaded_signature_to_report_task_completed_works(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        model_attach = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        self.api_work_tasks.post_add_uploaded_signature_to_report_task_completed_works(
            model_task.id,
            model_attach.attachmentID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list technicians from task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24982")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24982)
    def test_get_list_technicians_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.get_list_technicians_task_completed_work(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list technicians from task completed work by completed work ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24983")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24983)
    def test_get_list_technicians_task_completed_work_completed_work_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.get_list_technicians_task_completed_work_completed_work_id(
            model_task.id,
            model_completed_work.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete technicians task completed works by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24985")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24985)
    def test_delete_technicians_task_completed_works_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        model_technicians = self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.delete_technicians_task_completed_works_by_list(
            model_technicians.results[0].taskID,
            model_technicians.results[0].completedWorkID,
            model_technicians.results[0].userID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list materials all task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24955")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24955)
    def test_get_list_materials_all_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventory_id = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name,
        )
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_materials_task_completed_work(
            task_id=model_task.id,
            completed_work_id=model_completed_work.result[0].id,
            material_id=materials_data.id,
            warehouse_id=wh_data.id,
            inventory_id=model_inventory_id.result[0].id,
            measurement_unit_id=materials_data.measurementUnitID,
            user_id=model_api_user.user.id
        )
        self.api_work_tasks.get_list_materials_all_task_completed_work(model_task.id)
        self.api_work_tasks.delete_materials_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            materials_data.id,
            wh_data.id,
            model_inventory_id.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_wh_materials.delete_materials_by_list(materials_data.id)
        self.api_wh_warehouses.delete_warehouses_by_list(wh_data.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test update technician task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24987")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24987)
    def test_put_update_technician_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.put_update_technician_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete technicians task completed work.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24988")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24988)
    def test_delete_technicians_task_completed_work(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_completed_work = self.api_work_completed_works.post_add_completed_works(
            task_id=model_task.id,
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_work_tasks.post_add_technicians_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.delete_technicians_from_task_completed_work(
            model_task.id,
            model_completed_work.result[0].id,
            model_user.userID
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_adm_users.delete_user_by_id(model_user.userID)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list contacts from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24989")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24989)
    def test_get_list_contacts_from_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, contact_id.contact[0])
        self.api_work_tasks.get_list_contacts_from_task(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get contact from task by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24990")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24990)
    def test_get_contact_from_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, contact_id.contact[0])
        self.api_work_tasks.get_contact_from_task_by_id(model_task.id, contact_id.contact[0])
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete contact from task by contact id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24994")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24994)
    def test_delete_contact_from_task_by_contact_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_task_contacts.post_add_contacts_to_task(model_task.id, contact_id.contact[0])
        self.api_work_tasks.delete_contact_from_task_by_contact_id(model_task.id, contact_id.contact[0])
        model_contact = self.api_work_tasks.get_contact_from_task_by_id(model_task.id, contact_id.contact[0])
        assert hasattr(model_contact, 'deleted'), \
            f'Contact with ID {contact_id.contact[0]} not deleted from task ID {model_task.id}'
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get list conversations from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24998")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24998)
    def test_get_list_conversations_from_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_conversation = self.api_work_tasks.post_add_conversation_to_task(
            model_task.id,
            False
        )
        model_conversation_get = self.api_work_tasks.get_conversations_from_task(model_task.id)
        assert model_conversation.result[0].id == model_conversation_get.results[0].id, \
            (f'Expected conversation ID {model_conversation.result[0].id}, '
             f'but got {model_conversation_get.results[0].id}')
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get head conversations from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25056")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25056)
    def test_head_conversations_from_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_conversation = self.api_work_tasks.post_add_conversation_to_task(
            model_task.id,
            False
        )
        model_conversation_2 = self.api_work_tasks.post_add_conversation_to_task(
            model_task.id,
            False
        )
        model_conversation_3 = self.api_work_tasks.post_add_conversation_to_task(
            model_task.id,
            False
        )
        model_conversation_get = self.api_work_tasks.get_conversations_from_task(model_task.id)
        assert model_conversation.result[0].id == model_conversation_get.results[0].id, \
            (f'Expected conversation ID {model_conversation.result[0].id}, '
             f'but got {model_conversation_get.results[0].id}')
        assert model_conversation_2.result[0].id == model_conversation_get.results[1].id, \
            (f'Expected conversation ID {model_conversation_2.result[0].id}, '
             f'but got {model_conversation_get.results[1].id}')
        assert model_conversation_3.result[0].id == model_conversation_get.results[2].id, \
            (f'Expected conversation ID {model_conversation_3.result[0].id}, '
             f'but got {model_conversation_get.results[2].id}')
        head_conversations_qty = self.api_work_tasks.head_conversations_from_task(model_task.id)
        assert len(model_conversation_get.results) == head_conversations_qty, \
            f'The list of conversation headers does not match the actual value'
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get conversation by ID from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25065")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25065)
    def test_get_conversation_from_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_conversation = self.api_work_tasks.post_add_conversation_to_task(
            model_task.id,
            False
        )
        model_conversation_get = self.api_work_tasks.get_conversation_from_task_by_id(
            model_task.id,
            model_conversation.result[0].id
        )
        assert model_conversation.result[0].id == model_conversation_get.id, \
            (f'Expected conversation ID {model_conversation.result[0].id}, '
             f'but got {model_conversation_get.id}')
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test upload file to server and bind to conversation task, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25066")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25066)
    def test_post_upload_attachment_to_server_bind_conversation_task_data_from_form(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_conversation_task_data_from_form(
            model_task.id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test download attachment from conversation task by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25067")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25067)
    def test_get_download_attachment_from_conversation_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_attach = self.api_work_tasks.post_upload_attachment_to_server_bind_conversation_task_data_from_form(
            model_task.id
        )
        self.api_work_tasks.get_download_attachment_from_conversation_task_by_id(
            model_task.id,
            model_attach.taskconversationID,
            model_attach.attachments[0]
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachments[0])
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get info conversation delivery from task by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25068")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25068)
    def test_get_info_conversation_delivery_from_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_conversation = self.api_work_tasks.post_add_conversation_to_task(
            model_task.id,
            False
        )
        self.api_work_tasks.get_info_conversation_delivery_from_task_by_id(
            model_task.id,
            model_conversation.result[0].id
        )
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test update (PATCH) Notes field in the task by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25069")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25069)
    def test_patch_update_field_notes_in_task_by_id(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_path = self.api_work_tasks.patch_update_field_notes_in_task_by_id(model_task.id)
        model_get_task = self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        assert model_path == model_get_task.notes, \
            f'Expected {model_path}, but got {model_get_task.notes}.'
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test delete four task by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25084")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25084)
    def test_delete_task_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task1 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task2 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task3 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.delete_task_by_list(
            model_task.id, model_task1.id, model_task2.id, model_task3.id
        )
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get info the company code is used when generating the task number.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25086")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25086)
    def test_get_info_check_company_code_used(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_code = self.api_work_tasks.get_info_check_company_code_used(model_task.id)
        assert task_type_id[2] == model_code.result, \
            f'Expected {task_type_id[2]}, but got {model_code.result}.'
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test head task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25087")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25087)
    def test_head_task(self):
        self.api_work_tasks.head_task()

    @allure.title('Test get short list tasks.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25088")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25088)
    def test_get_short_list_tasks(self):
        self.api_work_tasks.get_short_list_tasks()

    @allure.title('Test get list of available stages to which the task can be transferred.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23709")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23709)
    def test_get_list_task_stages_next(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.get_list_task_stages_next(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

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
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

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
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

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
        self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

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
        task_number, note_task = self.api_work_tasks.put_update_task_by_id(model_task.id)
        model_info_task = self.api_work_tasks.get_detailed_info_task_by_id(model_task.id)
        assert model_info_task.number == task_number, f'Expected {model_info_task.number}, but got {task_number}'
        assert model_info_task.notes == note_task, f'Expected {model_info_task.notes}, but got {note_task}'
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test marks the task as completed.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25089")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25089)
    def test_put_task_completed(self, bearer_token):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.put_task_completed(model_task.id, bearer_token)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test restore deleted task by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25091")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25091)
    def test_put_restore_deleted_tasks_by_list(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task1 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task2 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        model_task3 = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.delete_task_by_list(
            model_task.id, model_task1.id, model_task2.id, model_task3.id
        )
        self.api_work_tasks.put_restore_deleted_tasks_by_list(
            model_task.id, model_task1.id, model_task2.id, model_task3.id
        )
        self.api_work_tasks.delete_task_by_list(
            model_task.id, model_task1.id, model_task2.id, model_task3.id
        )
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get count list tasks by day (yesterday, now).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25092")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25092)
    def test_get_count_list_tasks_by_day(self):
        self.api_work_tasks.get_count_list_tasks_by_day()

    @allure.title('Test get short list of tasks clustered by geo-area hash code (clustering).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25095")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25095)
    def test_get_short_list_tasks_by_geo_area_hash_code(self):
        self.api_work_tasks.get_short_list_tasks_by_geo_area_hash_code()

    @allure.title('Test get list materials of task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25097")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25097)
    def test_get_list_materials_task(self):
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
        model_task_materials = self.api_work_task_materials.post_task_materials(
            model_task.id,
            model_materials.result[0],
            model_wh[0].result[0]
        )
        self.api_work_tasks.get_list_materials_task(model_task.id)
        self.api_work_task_materials.delete_task_materials(model_task.id, model_task_materials.result[0].id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test get metadata for the task form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25098")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25098)
    def test_get_metadata_for_task_form(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
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
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        self.api_work_tasks.get_metadata_for_task_form(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test get metadata for the task form (new).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25099")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25099)
    def test_get_metadata_for_tasks_form_new(self):
        self.api_work_tasks.get_metadata_for_tasks_form_new()

    @allure.title('Test get technician reviews/ratings on the task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25100")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25100)
    def test_get_technician_ratings_avg_on_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
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
        self.api_work_task_assignment_history.post_add_new_task_to_user(model_user.userID, model_task.id)
        self.api_work_task_ratings.post_task_ratings(model_task.id)
        self.api_work_tasks.get_technician_ratings_avg_on_task(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get technician ratings on the task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25101")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25101)
    def test_get_technician_ratings_on_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
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
        self.api_work_task_assignment_history.post_add_new_task_to_user(model_user.userID, model_task.id)
        self.api_work_task_ratings.post_task_ratings(model_task.id)
        self.api_work_tasks.get_technician_ratings_on_task(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get skills from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25104")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25104)
    def test_get_skills_from_task(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_skills = self.api_pa_skills.post_add_skills_to_tenant()
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
        self.api_work_task_skills.post_add_skills_to_task(model_task.id, model_skills.skills[0].skillID)
        self.api_work_tasks.get_skills_from_task(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_pa_skills.delete_skill_by_id(model_skills.skills[0].skillID)

    @allure.title('Test activates the scheduled automatic transition through the task stages.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25041")
    @pytest.mark.skip(reason="Test development delayed")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25041)
    def test_post_activate_task_auto_staging(self):
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
        self.api_work_tasks.post_activate_task_auto_staging(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test deactivate the scheduled automatic transition through the task stages.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25042")
    @pytest.mark.skip(reason="Test development delayed")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25042)
    def test_delete_deactivate_task_auto_staging(self):
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
        self.api_work_tasks.post_activate_task_auto_staging(model_task.id)
        self.api_work_tasks.delete_deactivate_task_auto_staging(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get the history of the tasks movement through the stages.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25105")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25105)
    def test_get_task_stages(self):
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
        self.api_work_tasks.get_task_stages(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list of available stages to which tasks from the list can be transferred.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25106")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25106)
    def test_get_task_stages_next(self):
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
        self.api_work_tasks.get_task_stages_next(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get task tags.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25109")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25109)
    def test_get_task_tags(self):
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
        self.api_work_task_tags.post_add_tags_to_task(model_task.id)
        self.api_work_tasks.get_task_tags(model_task.id)
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get task watch lists.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25110")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25110)
    def test_get_task_watch_lists(self):
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        model_user = self.api_adm_users.post_add_user_staff()
        model_api_user = self.api_adm_tenant_members.get_api_user_in_current_tenant()
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
        self.api_work_task_assignment_history.post_add_new_task_to_user(model_user.userID, model_task.id)
        model_watch_lists = self.api_work_tasks.get_task_watch_lists(model_task.id)
        assert model_watch_lists.results[0].id == model_api_user.user.id, \
            f"Expected {model_watch_lists.results[0].id}, but got {model_api_user.user.id}"
        assert model_watch_lists.results[1].id == model_user.userID, \
            f"Expected {model_watch_lists.results[1].id}, but got {model_user.userID}"
        self.api_work_tasks.delete_task_by_id(model_task.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    class TestRequirement24586(BaseTest):

        @allure.title('Test POST add task with task number of different length.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25138")
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24586")
        @pytest.mark.regress
        @pytest.mark.parametrize('number, status_code, len_number', Params.params_post_task_number.value)
        @pytest.mark.test_case_id(25138)
        def test_post_add_task_with_number_of_different_length(self, number, status_code, len_number):
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
            try:
                model_task = self.api_work_tasks.post_add_task_with_number(
                    criticality_id=criticality_id,
                    task_type_id=task_type_id[0],
                    asset_id=object_model.id,
                    work_type_id=work_type_id,
                    company_id=company_id,
                    task_number=number,
                    status_code=status_code,
                    len_task_number=len_number
                )
                if model_task:
                    self.api_work_tasks.delete_task_by_id(model_task.id)
            finally:
                self.api_es_assets.delete_object_by_id(object_model.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

        @allure.title('Test PUT update task number on different length.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25139")
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24586")
        @pytest.mark.regress
        @pytest.mark.parametrize('number, status_code, len_number', Params.params_put_task_number.value)
        @pytest.mark.test_case_id(25139)
        def test_put_update_task_number_on_different_length(self, number, status_code, len_number):
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
                self.api_work_tasks.put_update_task_number(
                    task_id=model_task.id,
                    task_number=number,
                    status_code=status_code,
                    len_task_number=len_number
                )
            finally:
                self.api_work_tasks.delete_task_by_id(model_task.id)
                self.api_es_assets.delete_object_by_id(object_model.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

        @allure.title('Test PATCH update task number on different length.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25140")
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24586")
        @pytest.mark.regress
        @pytest.mark.parametrize('number, status_code, len_number', Params.params_patch_task_number.value)
        @pytest.mark.test_case_id(25140)
        def test_patch_update_task_number_on_different_length(self, number, status_code, len_number):
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
                self.api_work_tasks.patch_update_field_number_in_task_by_id(
                    task_id=model_task.id,
                    task_number=number,
                    status_code=status_code,
                    len_task_number=len_number
                )
            finally:
                self.api_work_tasks.delete_task_by_id(model_task.id)
                self.api_es_assets.delete_object_by_id(object_model.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

        @allure.title('Test export task with number with different length.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25143")
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24586")
        @pytest.mark.regress
        @pytest.mark.parametrize('number, status_code, len_number', Params.params_export_task_number.value)
        @pytest.mark.test_case_id(25143)
        def test_export_task_number_with_different_length(self, number, status_code, len_number):
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
            model_task = self.api_work_tasks.post_add_task_with_number(
                criticality_id=criticality_id,
                task_type_id=task_type_id[0],
                asset_id=object_model.id,
                work_type_id=work_type_id,
                company_id=company_id,
                task_number=number,
                status_code=status_code,
                len_task_number=len_number
            )
            try:
                self.api_export_tasks.get_normal_export_task_by_task_id(
                    task_id=model_task.id,
                    number_task=str(number),
                    name_task_type=task_type_id[1]
                )
            finally:
                if model_task:
                    self.api_work_tasks.delete_task_by_id(model_task.id)
                self.api_es_assets.delete_object_by_id(object_model.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)
