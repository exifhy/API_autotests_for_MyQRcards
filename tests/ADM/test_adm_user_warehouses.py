import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
@pytest.mark.xdist_group(name="many_users")
class TestAdmUserWarehouses(BaseTest):
    ...

    # @allure.title('Test add warehouses to user (deprecated).')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26210")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(26210)
    # @pytest.mark.skip(reason="Тест проходит в - test_delete_warehouses_from_user")
    # def test_post_add_warehouses_to_user(self):
    #     model_owner_user = self.api_adm_tenants.get_data_current_tenant()
    #     model_warehouses = self.api_wh_warehouses.post_add_warehouses()
    #     self.api_adm_user_warehouses.post_add_warehouses_to_user(
    #         model_owner_user.owner.userID,
    #         model_warehouses[0].result[0]
    #     )
    #     self.api_wh_warehouses.delete_warehouse_by_id(model_warehouses[0].result[0])

    # @allure.title('Test delete warehouses from user (deprecated).')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26211")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(26211)
    # def test_delete_warehouses_from_user(self):
    #     model_owner_user = self.api_adm_tenants.get_data_current_tenant()
    #     model_warehouses = self.api_wh_warehouses.post_add_warehouses()
    #     self.api_adm_user_warehouses.post_add_warehouses_to_user(
    #         model_owner_user.owner.userID,
    #         model_warehouses[0].result[0]
    #     )
    #     self.api_adm_user_warehouses.delete_warehouses_from_user(
    #         model_owner_user.owner.userID,
    #         model_warehouses[0].result[0]
    #     )
    #     self.api_wh_warehouses.delete_warehouse_by_id(model_warehouses[0].result[0])
