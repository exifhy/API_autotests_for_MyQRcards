import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserTemplates(BaseTest):

    @allure.title('Test get list user templates.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25789")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25789)
    def test_get_list_user_templates(self):
        self.api_adm_user_templates.get_list_user_templates()

    # @allure.title('Test add user template.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25791")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25791)
    # @pytest.mark.skip(reason="Тест на создание проходит в - test_delete_user_template_by_id")
    # def test_post_add_user_template(self):
    #     model_template = self.api_adm_user_templates.post_add_user_template()
    #     self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test delete user template by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25792")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25792)
    def test_delete_user_template_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test update user template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25793")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25793)
    def test_put_update_user_template(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        self.api_adm_user_templates.put_update_user_template(model_template.results[0])
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test get user template by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25794")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25794)
    def test_get_user_template_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        self.api_adm_user_templates.get_user_template_by_id(model_template.results[0])
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test delete three user templates by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25795")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25795)
    def test_delete_three_user_templates_by_list(self):
        model_template = self.api_adm_user_templates.post_add_three_user_templates()
        self.api_adm_user_templates.delete_user_templates_by_list(
            model_template.results[0],
            model_template.results[1],
            model_template.results[2]
        )

    @allure.title('Test get roles user template by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25797")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25797)
    def test_get_roles_user_template_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_roles = self.api_adm_roles.get_list_roles()
        self.api_adm_user_template_roles.post_add_user_template_roles(
            model_template.results[0],
            model_roles.results[0].id
        )
        self.api_adm_user_templates.get_roles_user_template_by_id(model_template.results[0])
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test get districts user template by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25796")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25796)
    def test_get_districts_user_template_by_id(self):
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_district = self.api_es_districts.post_add_district()
        self.api_adm_user_template_districts.post_add_user_template_districts(
            model_template.results[0],
            model_district.districts[0]
        )
        self.api_adm_user_templates.get_districts_user_template_by_id(model_template.results[0])
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])
        self.api_es_districts.delete_district_by_id(model_district.districts[0])
