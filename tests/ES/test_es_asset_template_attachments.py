import allure
import pytest
from allure_commons.types import Severity
from loguru import logger
from requests import JSONDecodeError

from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTemplateAttachments(BaseTest):

    @allure.title('Test bind attachments to asset templates by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24172")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24172)
    def test_post_bind_attachments_to_asset_template(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        model_attachment = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        try:
            self.api_es_asset_template_attachments.post_bind_attachments_to_asset_template(
                model_template.result[0],
                model_attachment.attachmentID
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachmentID)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete attachments from asset templates by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24171")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24171)
    def test_delete_attachments_from_asset_template(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        model_attachment = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        try:
            self.api_es_asset_template_attachments.post_bind_attachments_to_asset_template(
                model_template.result[0],
                model_attachment.attachmentID
            )
            self.api_es_asset_template_attachments.delete_attachments_from_asset_template(
                model_template.result[0],
                model_attachment.attachmentID
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachmentID)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test upload and bind attachment to asset template data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24144")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24144)
    def test_post_upload_and_bind_to_asset_template_data_from_form(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        try:
            model_attachment = self.api_es_asset_template_attachments.post_upload_and_bind_to_asset_template_data_from_form(
                model_template.result[0]
            )
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachmentID)
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test upload and bind attachment to asset template data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24174")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24174)
    def test_post_upload_bind_attachment_to_asset_template_data_from_body(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        try:
            model_attachment = self.api_es_asset_template_attachments.post_upload_bind_attachment_to_asset_template_data_from_body(
                model_template.result[0]
            )
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachmentID)
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)


@pytest.mark.test_scripts_suites_es_asset_template_attachments
class TestEsAssetTemplateAttachmentsScriptSuite(BaseTest):

    @allure.title(
        'Test script ES/assetTemplateAttachments (POST from form, GET, GET by id, DELETE by list, GET, GET by id).'
    )
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    def test_es_asset_template_attach_from_form_add_get_get_by_id_delete_by_list_get_get_by_id(
            self, request, return_func_name
    ):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    template_attach = self.api_es_asset_template_attachments.post_upload_and_bind_to_asset_template_data_from_form(
                        model_template.result[0]
                    )
                    model_get_list_attach = self.api_es_asset_templates.get_list_attachments_from_asset_template(
                        model_template.result[0],
                        False
                    )
                    assert str(template_attach.attachmentID) in model_get_list_attach.root, \
                        f'Attachment with ID {template_attach.attachmentID} is not in list asset template attachments'
                    self.api_es_asset_templates.get_downloading_attachment_file_asset_template(
                        model_template.result[0],
                        template_attach.attachmentID,
                        template_attach.fileName
                    )
                    self.api_es_asset_template_attachments.delete_attachments_from_asset_template(
                        model_template.result[0],
                        template_attach.attachmentID
                    )
                    self.api_es_asset_templates.get_list_attachments_from_asset_template(
                        model_template.result[0],
                        True
                    )
                    self.api_es_asset_templates.get_deleted_attachment_file_asset_template_by_id(
                        model_template.result[0],
                        template_attach.attachmentID
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)
        self.api_common_attachments.delete_attachment_by_id(model_template.result[0])

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
