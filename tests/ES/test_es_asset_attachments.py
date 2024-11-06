import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetAttachments(BaseTest):

    @allure.title('Test bind attachments to asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23800")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23800)
    def test_post_bind_attachments_to_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        attachment_id = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        try:
            self.api_es_asset_attachments.post_bind_attachments_to_asset(
                model_asset.id,
                attachment_id.attachmentID
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)

    @allure.title('Test unbind attachments from asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23801")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23801)
    def test_delete_unbind_attachments_from_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        attachment_id = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        try:
            self.api_es_asset_attachments.post_bind_attachments_to_asset(
                model_asset.id,
                attachment_id.attachmentID
            )
            self.api_es_asset_attachments.delete_unbind_attachments_from_asset(
                model_asset.id,
                attachment_id.attachmentID
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)

    @allure.title('Test upload file to server and bind to asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23802")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23802)
    def test_post_upload_file_to_server_and_bind_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

        attachment_id = self.api_es_asset_attachments.post_upload_file_to_server_and_bind_asset(
            asset_id=model_asset.id
        )
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)

    @allure.title('Test upload file to server and bind to asset, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23806")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23806)
    def test_post_upload_file_to_server_and_bind_asset_data_from_form(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

        attachment_id = self.api_es_asset_attachments.post_upload_file_to_server_and_bind_asset_data_from_form(
            asset_id=model_asset.id
        )
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)
