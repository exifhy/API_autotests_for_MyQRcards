import allure
import pytest
import os
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("UI service for providing components and controls info for front-end application part.")
@pytest.mark.skipif(
    os.environ.get('TENANT_ID') not in ['121', '66', '405'],
    reason="Test only for tenants 121, 66, 405"
)
class TestUILayoutTemplates(BaseTest):

    @allure.title('Test get list task layout templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26977")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26977)
    def test_get_list_task_layout_templates(self):
        self.api_ui_layout_templates.get_list_task_layout_templates()

    @allure.title('Test create layout template without taskTypeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26978")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26978)
    def test_post_add_layout_template_without_task_type_id(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, None)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test create layout template with taskTypeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27098")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27098)
    def test_post_add_layout_template_with_task_type_id(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, task_type_id[0])
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test delete layout template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26981")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26981)
    def test_delete_layout_template_by_id(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, None)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test create a default layout template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27080")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27080)
    def test_post_default_layout_template(self):
        model_template_default = self.api_ui_layout_templates.get_list_task_layout_templates_with_is_default(True)
        if model_template_default is not None:
            self.api_ui_layout_templates.post_default_layout_template_already_exists()
        else:
            self.api_ui_layout_templates.post_default_layout_template_non_existent()

    @allure.title('Test get list task layout templates with taskTypeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27081")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27081)
    def test_get_list_task_layout_templates_with_task_type_id(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, task_type_id[0])
        self.api_ui_layout_templates.get_list_task_layout_templates_with_task_type_id(task_type_id[0])
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test get list task layout templates with isDefault.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27038")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27038)
    def test_get_list_task_layout_templates_with_is_default(self):
        self.api_ui_layout_templates.get_list_task_layout_templates_with_is_default(True)

    @allure.title('Test resets the layout template settings to the default template state.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26976")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26976)
    def test_put_reset_layout_template_to_default_state(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template_without_fields(False)
        self.api_ui_layout_templates.put_reset_layout_template_to_default_state(model_template.id)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test get task layout template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26979")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26979)
    def test_get_task_layout_template_by_id(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, None)
        self.api_ui_layout_templates.get_task_layout_template_by_id(model_template.id)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test get deleted task layout template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27085")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27085)
    def test_get_deleted_task_layout_template_by_id(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, None)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)
        self.api_ui_layout_templates.get_deleted_task_layout_template_by_id(model_template.id)

    @allure.title('Test get nonexistent task layout template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27086")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27086)
    def test_get_nonexistent_task_layout_template_by_id(self):
        self.api_ui_layout_templates.get_nonexistent_task_layout_template_by_id(9999999)

    @allure.title('Test create layout template with deleted taskTypeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27093")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27093)
    def test_post_add_layout_template_with_deleted_task_type(self):
        model_task_type = self.api_work_task_types.get_list_task_types()
        self.api_ui_layout_templates.post_add_layout_template_with_deleted_task_type(
            max(map(int, model_task_type.root.keys())) + 1
        )

    @allure.title('Test create layout template with nonexistent taskTypeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27096")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27096)
    def test_post_add_layout_template_with_nonexistent_task_type(self):
        self.api_ui_layout_templates.post_add_layout_template_with_nonexistent_task_type(False, 255)

    @allure.title('Test create layout template task types is already in use.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27099")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27099)
    def test_post_add_layout_template_task_type_is_already_in_use(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_ui_layout_templates.create_layout_template_task_type_is_already_in_use(int(task_type_id[0]))

    @allure.title('Test update layout template task types is already in use.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27119")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27119)
    def test_put_update_layout_template_task_type_is_already_in_use(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_ui_layout_templates.update_layout_template_task_type_is_already_in_use(int(task_type_id[0]))

    @allure.title('Test create layout template without fields.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27107")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27107)
    def test_post_add_layout_template_without_fields(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template_without_fields(False)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test update layout template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26980")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26980)
    def test_put_update_layout_template(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_template = self.api_ui_layout_templates.post_add_layout_template_without_fields(False)
        self.api_ui_layout_templates.put_update_layout_template(model_template.id, False, task_type_id[0])
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)

    @allure.title('Test update deleted layout template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27118")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27118)
    def test_put_update_deleted_layout_template(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_template = self.api_ui_layout_templates.post_add_layout_template_without_fields(False)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)
        self.api_ui_layout_templates.put_update_deleted_layout_template(model_template.id, False, task_type_id[0])

    @allure.title('Test resets default layout template settings to the default template state.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27120")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27120)
    def test_put_reset_default_layout_template_to_default_state(self):
        self.api_ui_layout_templates.put_reset_default_layout_template_to_default_state()

    @allure.title('Test reset deleted layout template settings to the default template state.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27121")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27121)
    def test_put_reset_deleted_layout_template_to_default_state(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, None)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)
        self.api_ui_layout_templates.put_reset_of_invalid_layout_template_to_default_state(model_template.id)

    @allure.title('Test reset nonexistent layout template settings to the default template state.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27122")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27122)
    def test_put_reset_nonexistent_layout_template_to_default_state(self):
        self.api_ui_layout_templates.put_reset_of_invalid_layout_template_to_default_state(999999999)

    @allure.title('Test delete deleted layout template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27123")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27123)
    def test_delete_deleted_layout_template_by_id(self):
        model_template = self.api_ui_layout_templates.post_add_layout_template(False, None)
        self.api_ui_layout_templates.delete_layout_template_by_id(model_template.id)
        self.api_ui_layout_templates.delete_invalid_layout_template_by_id(model_template.id)

    @allure.title('Test delete nonexistent layout template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27124")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27124)
    def test_delete_nonexistent_layout_template_by_id(self):
        self.api_ui_layout_templates.delete_invalid_layout_template_by_id(999999999)

    @allure.title('Test get layout template by type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26982")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26982)
    def test_get_layout_template_by_type_by_id(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        self.api_ui_layout_templates.get_layout_template_by_type_by_id(task_type_id[0])

    @allure.title('Test get nonexistent layout template by type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27125")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27125)
    def test_get_nonexistent_layout_template_by_type_by_id(self):
        model_task_type = self.api_work_task_types.get_list_task_types()
        self.api_ui_layout_templates.get_nonexistent_layout_template_by_type_by_id(
            max(map(int, model_task_type.root.keys())) + 254
        )

    @allure.title('Test get deleted layout template by type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/27126")
    @pytest.mark.regress
    @pytest.mark.test_case_id(27126)
    def test_get_deleted_layout_template_by_type_by_id(self):
        model_task_type = self.api_work_task_types.get_list_task_types()
        self.api_ui_layout_templates.get_deleted_layout_template_by_type_by_id(
            max(map(int, model_task_type.root.keys())) + 1
        )
