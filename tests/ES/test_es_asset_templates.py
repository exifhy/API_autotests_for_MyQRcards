import allure
import pytest
from allure_commons.types import Severity
from loguru import logger
from pydantic_core import ValidationError
from requests import JSONDecodeError

from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetTemplates(BaseTest):

    @allure.title('Test add asset templates with asset type, asset class, location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24139")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24139)
    def test_post_add_asset_templates(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        try:
            model_template = self.api_es_asset_templates.post_add_asset_templates(
                asset_type_id, asset_class_id, location_id
            )
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
        finally:
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete asset templates by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24152")
    @pytest.mark.skip(reason="Тест на удаление шаблона списком проходит в - test_post_add_asset_templates")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24152)
    def test_delete_asset_templates_by_list(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        try:
            model_template = self.api_es_asset_templates.post_add_asset_templates(
                asset_type_id, asset_class_id, location_id
            )
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
        finally:
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete asset template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24154")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24154)
    def test_delete_asset_template_by_id(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        try:
            model_template = self.api_es_asset_templates.post_add_asset_templates(
                asset_type_id, asset_class_id, location_id
            )
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        finally:
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list attachments from asset template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24140")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24140)
    def test_get_list_attachments_from_asset_template(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        model_attachment = self.api_es_asset_template_attachments.post_upload_and_bind_to_asset_template_data_from_form(
            model_template.result[0]
        )
        try:
            self.api_es_asset_templates.get_list_attachments_from_asset_template(
                model_template.result[0],
                False
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachmentID)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list attributes from asset template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24165")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24165)
    def test_get_list_attributes_from_asset_template(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_asset_str()
        self.api_es_asset_template_attributes.post_update_attributes_asset_templates(
            model_template.result[0],
            attribute_id.values[0]
        )
        try:
            self.api_es_asset_templates.get_list_attributes_from_asset_template(model_template.result[0], False)
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test method to get TemporaryRedirect to a temporary link for downloading the attachment file.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24145")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24145)
    def test_get_downloading_attachment_file_asset_template(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        model_attachment = self.api_es_asset_template_attachments.post_upload_and_bind_to_asset_template_data_from_form(
            model_template.result[0]
        )
        try:
            self.api_es_asset_templates.get_downloading_attachment_file_asset_template(
                model_template.result[0],
                model_attachment.attachmentID,
                model_attachment.fileName
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attachments.delete_attachment_by_id(model_attachment.attachmentID)

    @allure.title('Test upload avatar(jpeg > 512x512) to asset template, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24146")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24146)
    def test_put_upload_avatar_to_asset_template_data_from_form(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        try:
            self.api_es_asset_templates.put_upload_avatar_to_asset_template_data_from_form(
                model_template.result[0]
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test upload avatar(jpeg > 512x512) to asset template, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24147")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24147)
    def test_put_upload_avatar_to_asset_template_data_from_body(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        try:
            self.api_es_asset_templates.put_upload_avatar_to_asset_template_data_from_body(
                model_template.result[0]
            )
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete avatar from the asset template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24148")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24148)
    def test_delete_avatar_from_asset_template(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        self.api_es_asset_templates.put_upload_avatar_to_asset_template_data_from_body(
            model_template.result[0]
        )
        try:
            self.api_es_asset_templates.delete_avatar_from_asset_template(model_template.result[0])
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete avatar from the asset templates by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24149")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24149)
    def test_delete_avatar_from_asset_templates_by_list(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        self.api_es_asset_templates.put_upload_avatar_to_asset_template_data_from_body(
            model_template.result[0]
        )
        try:
            self.api_es_asset_templates.delete_avatar_from_asset_templates_by_list(model_template.result[0])
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24150")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24150)
    def test_get_list_asset_templates(self):
        self.api_es_asset_templates.get_list_asset_templates(None)

    @allure.title('Test update asset templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24151")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24151)
    def test_put_update_asset_templates(self):
        location_id_first = self.api_es_locations.post_add_location()
        location_id_second = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        template_id = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id_first
        )
        try:
            model_before = self.api_es_asset_templates.get_asset_template_by_id(template_id.result[0])
            self.api_es_asset_templates.put_update_asset_templates(
                asset_template_id=template_id.result[0],
                asset_type_id=None,
                asset_class_id=None,
                location_id=location_id_second
            )
            model_after = self.api_es_asset_templates.get_asset_template_by_id(template_id.result[0])

            assert model_before.name != model_after.name, \
                f'{model_before.name} is equal {model_after.name}'
            assert model_before.description != model_after.description, \
                f'{model_before.description} is equal {model_after.description}'
            assert model_before.location.address != model_after.location.address, \
                f'{model_before.location.address} is equal {model_after.location.address}'
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(template_id.result[0])
            self.api_es_locations.delete_location_by_id(location_id_first)
            self.api_es_locations.delete_location_by_id(location_id_second)

    @allure.title('Test get asset template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24153")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24153)
    def test_get_asset_template_by_id(self):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_template = self.api_es_asset_templates.post_add_asset_templates(
            asset_type_id, asset_class_id, location_id
        )
        try:
            self.api_es_asset_templates.get_asset_template_by_id(model_template.result[0])
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list districts from asset template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24158")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24158)
    def test_get_list_districts_from_asset_templates(self):
        district_id = self.api_es_districts.post_add_district()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_districts.post_districts_to_asset_templates(
            model_template.result[0],
            district_id.districts[0]
        )
        try:
            self.api_es_asset_templates.get_list_districts_from_asset_templates(model_template.result[0], False)
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test get list skills from asset template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24160")
    @pytest.mark.xfail(reason="500. Unable To Resolve")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24160)
    def test_get_list_skills_from_asset_templates(self):
        skill_id = self.api_pa_skills.get_list_skills_tenant_return_first_skills()
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        self.api_es_asset_template_skills.post_skills_to_asset_templates(
            model_template.result[0],
            skill_id
        )
        try:
            self.api_es_asset_templates.get_list_skills_from_asset_templates(model_template.result[0])
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])

    @allure.title('Test get list work types from asset template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24161")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24161)
    def test_get_list_work_types_from_asset_templates(self):
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        self.api_es_asset_template_work_types.post_add_work_types_to_asset_templates(
            model_template.result[0],
            work_type_id
        )
        try:
            self.api_es_asset_templates.get_list_work_types_from_asset_templates(model_template.result[0], False)
        finally:
            self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])


@pytest.mark.test_scripts_suites_es_asset_templates
class TestEsAssetTemplatesScriptSuite(BaseTest):

    @allure.title('Test api test script ES/assetTemplates (POST, GET, GET by id, DELETE by list, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24570")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24570)
    @pytest.mark.test_script_runs
    def test_es_asset_templates_add_get_get_by_id_delete_by_list_get_get_by_id(self, request, return_func_name):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    model_template = self.api_es_asset_templates.post_add_asset_templates(
                        asset_type_id, asset_class_id, location_id
                    )
                    self.api_es_asset_templates.get_list_asset_templates(model_template.result[0])
                    self.api_es_asset_templates.get_asset_template_by_id(model_template.result[0])
                    self.api_es_asset_templates.delete_asset_templates_by_list(model_template.result[0])
                    self.api_es_asset_templates.get_list_asset_templates_check_is_deleted(model_template.result[0])
                    self.api_es_asset_templates.get_deleted_asset_template_by_id(model_template.result[0])
                except (AssertionError, JSONDecodeError, ValidationError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assetTemplates (POST, GET, GET by id, DELETE by id, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24571")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24571)
    @pytest.mark.test_script_runs
    def test_es_asset_templates_add_get_get_by_id_delete_by_id_get_get_by_id(self, request, return_func_name):
        location_id = self.api_es_locations.post_add_location()
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    model_template = self.api_es_asset_templates.post_add_asset_templates(
                        asset_type_id, asset_class_id, location_id
                    )
                    self.api_es_asset_templates.get_list_asset_templates(model_template.result[0])
                    self.api_es_asset_templates.get_asset_template_by_id(model_template.result[0])
                    self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
                    self.api_es_asset_templates.get_list_asset_templates_check_is_deleted(model_template.result[0])
                    self.api_es_asset_templates.get_deleted_asset_template_by_id(model_template.result[0])
                except (AssertionError, JSONDecodeError, ValidationError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assetTemplates (PUT, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24572")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24572)
    @pytest.mark.test_script_runs
    def test_es_asset_templates_put_get_get_by_id(self, request, return_func_name):
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
                    model_before = self.api_es_asset_templates.get_asset_template_by_id(model_template.result[0])
                    self.api_es_asset_templates.put_update_asset_templates(
                        model_template.result[0], asset_type_id, asset_class_id, location_id
                    )
                    self.api_es_asset_templates.get_list_asset_templates_check_data(
                        model_before,
                        model_template.result[0]
                    )
                    model_after = self.api_es_asset_templates.get_asset_template_by_id(model_template.result[0])
                    assert model_before != model_after, \
                        f'{model_before} is equal {model_after}, template ID {model_template.result[0]} is not updated'
                except (AssertionError, JSONDecodeError, ValidationError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assetTemplates/avatar (PUT, GET by id, DELETE, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_asset_templates_avatar_put_get_by_id_delete_get_by_id(self, request, return_func_name):
        model_template = self.api_es_asset_templates.post_add_empty_asset_template()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    model_avatar = self.api_es_asset_templates.put_upload_avatar_to_asset_template_data_from_form(
                        model_template.result[0]
                    )
                    self.api_es_asset_templates.get_asset_template_by_id_check_avatar(
                        model_template.result[0],
                        model_avatar,
                        False
                    )
                    self.api_es_asset_templates.delete_avatar_from_asset_template(model_template.result[0])
                    self.api_es_asset_templates.get_asset_template_by_id_check_avatar(
                        model_template.result[0],
                        model_avatar,
                        True
                    )
                except (AssertionError, JSONDecodeError, ValidationError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
                finally:
                    self.api_common_attachments.delete_attachment_by_id(model_avatar.attachmentID)

        self.api_es_asset_templates.delete_asset_templates_by_id(model_template.result[0])

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
