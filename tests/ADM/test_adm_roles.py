import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params



@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRoles(BaseTest):

    @allure.title('Test get list roles.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25776")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25776)
    def test_get_list_roles(self):
        self.api_adm_roles.get_list_roles()

    @allure.title('Test get list applications role by role ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25863")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25863)
    def test_get_list_applications_role_by_role_id(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_list_applications_role_by_role_id(model_role.results[0].id)

    # @allure.title('Test get list attachments role by role ID.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25864")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25864)
    # @pytest.mark.skip(reason="Ручка отключена.")
    # def test_get_list_attachments_role_by_role_id(self):
    #     model_role = self.api_adm_roles.get_list_roles()
    #     self.api_adm_roles.get_list_attachments_role_by_role_id(model_role.results[0].id)

    @allure.title('Test get role by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25865")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25865)
    def test_get_role_by_id(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_by_id(model_role.results[0].id)

    @allure.title('Test delete role by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25866")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25866)
    def test_delete_role_by_id(self):
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_roles.delete_role_by_id(model_role.results[0])

    # @allure.title('Test add role.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25867")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25867)
    # @pytest.mark.skip(reason="Тест на создание проходит в - test_delete_role_by_id")
    # def test_post_add_role(self):
    #     model_role = self.api_adm_roles.post_add_role()
    #     self.api_adm_roles.delete_roles_by_list(model_role.results[0])

    @allure.title('Test update role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25869")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25869)
    def test_put_update_role(self):
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_roles.put_update_role(model_role.results[0])
        self.api_adm_roles.delete_roles_by_list(model_role.results[0])

    @allure.title('Test delete three roles by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25870")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25870)
    def test_delete_roles_by_list(self):
        model_role = self.api_adm_roles.post_add_three_roles()
        self.api_adm_roles.delete_roles_by_list(
            model_role.results[0],
            model_role.results[1],
            model_role.results[2]
        )

    @allure.title('Test copy role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25871")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25871)
    def test_post_copy_role(self):
        model_role = self.api_adm_roles.get_list_roles()
        model_copy = self.api_adm_roles.post_copy_roles(model_role.results[0].id)
        self.api_adm_roles.delete_roles_by_list(model_copy.results[0])

    @allure.title('Test get list role permissions api')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25872")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25872)
    def test_get_role_permissions_api(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_permissions_api(model_role.results[0].id)

    @allure.title('Test get list role permissions ext')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25873")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25873)
    def test_get_role_permissions_ext(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_permissions_ext(model_role.results[0].id)

    @allure.title('Test get list role permissions UI')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25874")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25874)
    def test_get_role_permissions_ui(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_permissions_ui(model_role.results[0].id)

    @allure.title('Test add package to role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30323")
    @pytest.mark.skip(reason="Плагин автоматически добавляется к существующей роли.")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30323)
    def test_post_add_roles_packages(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        model_package_role = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            model_package_role = self.api_adm_roles.post_add_roles_packages(
                role_id,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )
        finally:
            if model_package_role:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    model_package_role.results[0].id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test get list roles packages by role ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30313")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30313)
    def test_get_list_roles_packages_by_id(self):
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        self.api_adm_roles.get_list_roles_packages_by_id(role_id)
    
    @allure.title('Test get list roles packages without token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30314")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_roles_packages_without_token(self):
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        self.api_adm_roles.get_list_roles_packages_without_token(role_id)

    @allure.title('Test get list roles packages with invalid token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30315")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_roles_packages_invalid_token(self):
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        self.api_adm_roles.get_list_roles_packages_invalid_token(role_id)

    @allure.title('Test get list roles packages verify forbidden access.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30316")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30316)
    def test_get_list_roles_packages_forbidden(self):
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        self.api_adm_roles.get_list_roles_packages_forbidden(role_id)

    @allure.title('Test get list roles packages with invalid app id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30317")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30317)
    def test_get_list_roles_packages_invalid_app_id(self):
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        self.api_adm_roles.get_list_roles_packages_invalid_app_id(role_id)
    
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30318")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30318)
    @pytest.mark.parametrize('content_type', Params.params_content_type_body.value)
    def test_get_list_roles_packages_with_content_type(self, content_type, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
        self.api_adm_roles.get_list_roles_packages_with_content_type(role_id, content_type)

    @allure.title('Test get list roles packages measure response time.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30319")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30319)
    def test_get_list_roles_packages_measure_time(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            self.api_adm_roles.get_list_roles_packages_measure_time(role_id, 200)

            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test get list roles packages idempotency.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30320")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30320)
    def test_get_list_roles_packages_idempotent(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            self.api_adm_roles.get_list_roles_packages_idempotent(role_id)

            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test get list roles packages concurrent requests.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30321")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30321)
    def test_get_list_roles_packages_concurrent(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            self.api_adm_roles.get_list_roles_packages_concurrent(role_id)

            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test get list roles packages with range/fetch.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30322")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30322)
    def test_get_list_roles_packages_with_range_and_fetch(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            self.api_adm_roles.get_list_roles_packages_with_range_and_fetch(role_id)

            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test delete package from role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30324")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30324)
    def test_delete_packages_from_role(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test activate role packages.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30325")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30325)
    def test_put_roles_packages_activate(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
            self.api_adm_roles.put_roles_packages_activate(
                role_id,
                role_package_id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )

    @allure.title('Test deactivate role packages.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30326")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30326)
    def test_put_roles_packages_deactivate(self, bearer_token_power_user):
        model_tenant_package = None
        model_package = None
        role_package_id = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
                bearer_token_power_user
            )
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            role_package_id = self.api_adm_roles.get_list_roles_packages_by_id_return_role_package(
                role_id, model_package.results[0].package.id
            )
            self.api_adm_roles.put_roles_packages_activate(
                role_id,
                role_package_id
            )
            self.api_adm_roles.put_roles_packages_deactivate(
                role_id,
                role_package_id
            )
        finally:
            if role_package_id:
                self.api_adm_roles.delete_roles_packages_by_id(
                    role_id,
                    role_package_id
                )
            if model_tenant_package:
                self.api_adm_tenants.delete_package_from_tenant(
                    model_tenant_package.results[0].package.id,
                    model_tenant_package.results[0].package.version
                )
            if model_package:
                self.api_adm_tenants.delete_packages_from_system(
                    bearer_token_power_user,
                    model_package.results[0].package.id,
                    model_package.results[0].package.version
                )