import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskAttachmentsAPI(BaseTest):

    @allure.title('Test adds a uploaded attachments file to a task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24364")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24364)
    def test_post_task_attachments(self):
        # created_location_id = self.api_es_locations.post_add_location()
        # company_id = self.api_es_companies.post_add_our_company()
        # location_id = self.api_es_locations.post_add_location()
        attachment_id = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        # self.api_es_company_locations.post_add_company_locations(
        #     company_id=company_id,
        #     location_id=location_id
        # )
        # asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        # asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        # work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        # object_model = self.api_es_assets.post_add_object(
        #     company_id=company_id,
        #     asset_class_id=asset_class_id,
        #     asset_type_id=asset_type_id
        # )
        # self.api_es_asset_work_types.post_add_work_type_to_asset(
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id
        # )
        # self.api_es_assetlocations.add_location_to_object(
        #     asset_id=object_model.id,
        #     location_id=created_location_id
        # )
        # self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        # self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        # criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        # model_task = self.api_work_tasks.post_add_task(
        #     criticality_id=criticality_id,
        #     task_type_id=task_type_id[0],
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id,
        #     company_id=company_id
        # )
        try:
            self.api_work_task_attachments.post_task_attachments(
                model_task.id,
                attachment_id.attachmentID
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
            # self.api_es_assets.delete_object_by_id(object_model.id)
            # self.api_es_companies.delete_company_by_id(company_id)
            # self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete uploaded attachments file from task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24365")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24365)
    def test_delete_task_attachments(self):
        # created_location_id = self.api_es_locations.post_add_location()
        # company_id = self.api_es_companies.post_add_our_company()
        # location_id = self.api_es_locations.post_add_location()
        # self.api_es_company_locations.post_add_company_locations(
        #     company_id=company_id,
        #     location_id=location_id
        # )
        # asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        # asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        # work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        # object_model = self.api_es_assets.post_add_object(
        #     company_id=company_id,
        #     asset_class_id=asset_class_id,
        #     asset_type_id=asset_type_id
        # )
        # self.api_es_asset_work_types.post_add_work_type_to_asset(
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id
        # )
        # self.api_es_assetlocations.add_location_to_object(
        #     asset_id=object_model.id,
        #     location_id=created_location_id
        # )
        # self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        # self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        # criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        # model_task = self.api_work_tasks.post_add_task(
        #     criticality_id=criticality_id,
        #     task_type_id=task_type_id[0],
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id,
        #     company_id=company_id
        # )
        try:
            attachment_id = self.api_work_task_attachments.post_upload_attachment_and_bind_to_task_data_from_form(
                model_task.id
            )
            self.api_work_task_attachments.delete_task_attachments(
                model_task.id,
                attachment_id.attachmentID
            )
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            # self.api_es_assets.delete_object_by_id(object_model.id)
            # self.api_es_companies.delete_company_by_id(company_id)
            # self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test uploads the file to server and binds it to the task, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24366")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24366)
    def test_post_upload_and_bind_to_task_data_from_form(self):
        # created_location_id = self.api_es_locations.post_add_location()
        # company_id = self.api_es_companies.post_add_our_company()
        # location_id = self.api_es_locations.post_add_location()
        # self.api_es_company_locations.post_add_company_locations(
        #     company_id=company_id,
        #     location_id=location_id
        # )
        # asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        # asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        # work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        # object_model = self.api_es_assets.post_add_object(
        #     company_id=company_id,
        #     asset_class_id=asset_class_id,
        #     asset_type_id=asset_type_id
        # )
        # self.api_es_asset_work_types.post_add_work_type_to_asset(
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id
        # )
        # self.api_es_assetlocations.add_location_to_object(
        #     asset_id=object_model.id,
        #     location_id=created_location_id
        # )
        # self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        # self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        # criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        # model_task = self.api_work_tasks.post_add_task(
        #     criticality_id=criticality_id,
        #     task_type_id=task_type_id[0],
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id,
        #     company_id=company_id
        # )
        try:
            attachment_id = self.api_work_task_attachments.post_upload_attachment_and_bind_to_task_data_from_form(
                model_task.id
            )
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            # self.api_es_assets.delete_object_by_id(object_model.id)
            # self.api_es_companies.delete_company_by_id(company_id)
            # self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test uploads the file to server and binds it to the task, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24367")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24367)
    def test_post_upload_and_bind_to_task_data_from_body(self):
        # created_location_id = self.api_es_locations.post_add_location()
        # company_id = self.api_es_companies.post_add_our_company()
        # location_id = self.api_es_locations.post_add_location()
        # self.api_es_company_locations.post_add_company_locations(
        #     company_id=company_id,
        #     location_id=location_id
        # )
        # asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        # asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        # work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        # object_model = self.api_es_assets.post_add_object(
        #     company_id=company_id,
        #     asset_class_id=asset_class_id,
        #     asset_type_id=asset_type_id
        # )
        # self.api_es_asset_work_types.post_add_work_type_to_asset(
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id
        # )
        # self.api_es_assetlocations.add_location_to_object(
        #     asset_id=object_model.id,
        #     location_id=created_location_id
        # )
        # self.api_es_asset_districts.add_default_district_to_object(object_model.id)
        # self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        # criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        # model_task = self.api_work_tasks.post_add_task(
        #     criticality_id=criticality_id,
        #     task_type_id=task_type_id[0],
        #     asset_id=object_model.id,
        #     work_type_id=work_type_id,
        #     company_id=company_id
        # )
        try:
            attachment_id = self.api_work_task_attachments.post_upload_bind_attachment_to_task_data_from_body(
                model_task.id
            )
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            # self.api_es_assets.delete_object_by_id(object_model.id)
            # self.api_es_companies.delete_company_by_id(company_id)
            # self.api_es_locations.delete_location_by_id(location_id)
