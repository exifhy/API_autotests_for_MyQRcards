import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmTenantMembers(BaseTest):

    @allure.title('Test get API user in the current tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23509")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23509)
    def test_get_api_user_in_current_tenant(self):
        self.api_adm_tenant_members.get_api_user_in_current_tenant()

    @allure.title('Test get tenant member this.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25916")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25916)
    def test_get_tenant_member_this(self):
        self.api_adm_tenant_members.get_tenant_member_this()

    @allure.title('Test get tenant member by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25914")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25914)
    def test_get_tenant_member_by_id(self):
        model_member = self.api_adm_tenant_members.get_list_tenant_members()
        self.api_adm_tenant_members.get_tenant_member_by_id(next(iter(model_member.root)))

    @allure.title('Test get list tenant members.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25917")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25917)
    def test_get_list_tenant_members(self):
        self.api_adm_tenant_members.get_list_tenant_members()

    @allure.title('Test get tenant members anonymous user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25920")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25920)
    def test_get_tenant_members_anonymous_user(self):
        model_anon = self.api_adm_tenant_members.get_tenant_members_anonymous_user()
        if model_anon is None:
            model_user = self.api_adm_users.post_add_anonymous_user()
            self.api_adm_tenant_members.get_tenant_members_anonymous_user()
            self.api_adm_users.delete_user_by_id(model_user.userID)
