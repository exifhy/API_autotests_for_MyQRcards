import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmTenants(BaseTest):

    @allure.title('Test get data current tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23882")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23882)
    def test_get_data_current_tenant(self):
        self.api_adm_tenants.get_data_current_tenant()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25615")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25615)
    @pytest.mark.parametrize('data, name_step, error_message', Params.params_negative_add_package_body.value)
    def test_post_add_package_to_database_negative(
            self, bearer_token_power_user, data, name_step, error_message, request
    ):
        allure.dynamic.title(f"{request.node.callspec.id}")
        self.api_adm_tenants.post_add_package_to_database_without_fields(
            bearer_token_power_user, data, name_step, error_message
        )

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25629")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25629)
    @pytest.mark.parametrize('resource_id, name, step_name, mobile',
                             Params.params_add_package_to_different_resource_body.value)
    def test_post_add_package_to_tenant_with_all_resource(
            self, bearer_token_power_user, resource_id, name, step_name, mobile, request
    ):
        allure.dynamic.title(f"{request.node.callspec.id}")
        model_package = self.api_adm_tenants.post_add_package_to_database_with_all_resource(
            bearer_token_power_user, resource_id, name, step_name, mobile
        )
        self.api_adm_tenants.post_add_package_to_tenant(
            model_package.results[0].package.id,
            model_package.results[0].package.version,
            mobile
        )
        self.api_adm_tenants.delete_packages_from_system(
            bearer_token_power_user,
            model_package.results[0].package.id,
            model_package.results[0].package.version
        )

    @allure.title('Test get list of tenants to which the authorized user has access.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25936")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25936)
    def test_get_list_tenants(self):
        self.api_adm_tenants.get_list_tenants()

    @allure.title('Test get list of template tenants to which the authenticated user has access.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25937")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25937)
    def test_get_list_templates_tenants(self):
        self.api_adm_tenants.get_list_templates_tenants()

    @allure.title('Test get list of feature flags tenants.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25938")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25938)
    def test_get_list_feature_flags_tenants(self):
        self.api_adm_tenants.get_list_feature_flags_tenants()

    @allure.title('Test get list of licenses tenants.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25939")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25939)
    def test_get_list_of_licenses_tenants(self):
        self.api_adm_tenants.get_list_of_licenses_tenants()

    @allure.title('Test get list meta from tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25945")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25945)
    def test_get_list_meta_from_tenant(self):
        self.api_adm_tenants.get_list_meta_from_tenant()

    @allure.title('Test get list packages from tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25639")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25639)
    def test_get_list_packages_from_tenant(self):
        self.api_adm_tenants.get_list_packages_from_tenant()

    @allure.title('Test add a package by cross tenant admin to database with the isMobile field, ResourceID=24.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25641")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25641)
    def test_post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
            bearer_token_power_user
        )
        self.api_adm_tenants.delete_packages_from_system(
            bearer_token_power_user,
            model_package.results[0].package.id,
            model_package.results[0].package.version
        )

    @allure.title('Test add a package by cross tenant admin to database without the isMobile field, ResourceID=1.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25642")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25642)
    def test_post_add_packages_to_data_base_cross_tenant_admin_without_mobile_field(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_without_mobile_field(
            bearer_token_power_user
        )
        self.api_adm_tenants.delete_packages_from_system(
            bearer_token_power_user,
            model_package.results[0].package.id,
            model_package.results[0].package.version
        )

    @allure.title('Test add a package by cross tenant admin to database with str in ResourceID filed.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25643")
    @pytest.mark.regress
    @pytest.mark.xfail(reason="Добавляет плагин со строкой в поле ResourceID, по схеме поле integer($int32).")
    @pytest.mark.test_case_id(25643)
    def test_post_add_packages_to_sys_tenant_admin_with_str_in_resource_id_field(self, bearer_token_power_user):
        model_package = None
        try:
            model_package = self.api_adm_tenants.post_add_packages_to_sys_cross_tenant_admin_with_str_in_resource_id_field(
                bearer_token_power_user
            )
        finally:
            self.api_adm_tenants.delete_packages_from_system(
                bearer_token_power_user,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )

    @allure.title('Test add a package without Authorization header.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25644")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25644)
    def test_post_add_package_without_authorization(self):
        self.api_adm_tenants.post_add_package_without_authorization()

    @allure.title('Test delete packages from system.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25645")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Удаление плагина из системы проходит "
                             "в - test_post_add_package_to_tenant_with_all_resource.")
    @pytest.mark.test_case_id(25645)
    def test_delete_packages_from_system(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
            bearer_token_power_user
        )
        self.api_adm_tenants.delete_packages_from_system(
            bearer_token_power_user,
            model_package.results[0].package.id,
            model_package.results[0].package.version
        )

    @allure.title('Test delete packages from system without Version field.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25646")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25646)
    def test_delete_packages_from_system_without_version_field(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
            bearer_token_power_user
        )
        try:
            self.api_adm_tenants.delete_packages_from_system_without_version_field(
                bearer_token_power_user,
                model_package.results[0].package.id
            )
        finally:
            self.api_adm_tenants.delete_packages_from_system(
                bearer_token_power_user,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )

    @allure.title('Test add a already exists package by cross tenant admin to system.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25647")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25647)
    def test_post_add_packages_to_system_cross_tenant_admin_already_exists(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
            bearer_token_power_user
        )
        try:
            self.api_adm_tenants.post_add_packages_to_system_cross_tenant_admin_already_exists(
                bearer_token_power_user,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )
        finally:
            self.api_adm_tenants.delete_packages_from_system(
                bearer_token_power_user,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )

    @allure.title('Test patch update a package by cross tenant admin.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25648")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25648)
    def test_patch_update_package_cross_tenant_admin(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
            bearer_token_power_user
        )
        try:
            self.api_adm_tenants.patch_update_package_cross_tenant_admin(
                bearer_token_power_user,
                model_package.results[0].package.id
            )
        finally:
            self.api_adm_tenants.delete_packages_from_system(
                bearer_token_power_user,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )

    @allure.title('Test delete a package from tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25649")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25649)
    def test_delete_package_from_tenant(self, bearer_token_power_user):
        model_package = self.api_adm_tenants.post_add_packages_to_data_base_cross_tenant_admin_with_is_mobile_field(
            bearer_token_power_user
        )
        try:
            model_tenant_package = self.api_adm_tenants.post_add_package_to_tenant(
                model_package.results[0].package.id,
                model_package.results[0].package.version,
                False
            )
            self.api_adm_tenants.delete_package_from_tenant(
                model_tenant_package.results[0].package.id,
                model_tenant_package.results[0].package.version
            )
        finally:
            self.api_adm_tenants.delete_packages_from_system(
                bearer_token_power_user,
                model_package.results[0].package.id,
                model_package.results[0].package.version
            )

    @allure.title('Test get a list variables from tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25946")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25946)
    def test_get_list_variables_from_tenant(self):
        self.api_adm_tenants.get_list_variables_from_tenant()

    @allure.title('Test add variables to tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25947")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25947)
    @pytest.mark.skip(reason="Тест на создание переменных проходит в - test_delete_variable_from_tenant_by_name")
    def test_post_add_variables_to_tenant(self):
        self.api_adm_tenants.post_add_variables_to_tenant()

    @allure.title('Test delete variable from tenant by name.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25951")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25951)
    def test_delete_variable_from_tenant_by_name(self):
        name = self.api_adm_tenants.post_add_variables_to_tenant()
        self.api_adm_tenants.delete_variable_from_tenant_by_name(name)

    @allure.title('Test delete variables from tenant by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25950")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25950)
    def test_delete_variables_from_tenant_by_list(self):
        name = self.api_adm_tenants.post_add_variables_to_tenant()
        name2 = self.api_adm_tenants.post_add_variables_to_tenant()
        name3 = self.api_adm_tenants.post_add_variables_to_tenant()
        self.api_adm_tenants.delete_variables_from_tenant_by_list(name, name2, name3)

    @allure.title('Test update variables tenant.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25949")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25949)
    def test_put_update_variables_tenant(self):
        name = self.api_adm_tenants.post_add_variables_to_tenant()
        self.api_adm_tenants.put_update_variables_tenant(name)
        self.api_adm_tenants.delete_variable_from_tenant_by_name(name)
