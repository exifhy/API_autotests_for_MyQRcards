import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWhWarehouses(BaseTest):

    @allure.title('Test add warehouses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24495")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на создание склада проходит в - test_delete_warehouses_by_list")
    @pytest.mark.test_case_id(24495)
    def test_post_add_warehouses(self):
        self.api_wh_warehouses.post_add_warehouses()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25353")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25353)
    @pytest.mark.parametrize('data, value_code, value_message, log_info', Params.params_negative_warehouse_body.value)
    def test_post_add_warehouse_negative(self, data, value_code, value_message, log_info, request):
        allure.dynamic.title(f"Test creating a warehouse - {request.node.callspec.id}")
        self.api_wh_warehouses.post_add_warehouse_parameterized_test(data, value_code, value_message, log_info)

    @allure.title('Test delete warehouses by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24496")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на удаление склада проходит в - test_get_warehouses_by_id")
    @pytest.mark.test_case_id(24496)
    def test_delete_warehouses_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test delete warehouse by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25363")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25363)
    def test_delete_warehouse_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test get warehouse by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24506")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24506)
    def test_get_warehouses_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test get list warehouse V2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25362")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25362)
    def test_get_list_warehouses_v2(self):
        self.api_wh_warehouses.get_list_warehouses_v2()

    @allure.title('Test get list warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25361")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25361)
    def test_get_list_warehouses(self):
        self.api_wh_warehouses.get_list_warehouses()

    @allure.title('Test head warehouses.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25359")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25359)
    def test_head_warehouses(self):
        self.api_wh_warehouses.head_warehouses()

    @allure.title('Test update warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25367")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25367)
    def test_put_update_warehouse(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.put_update_warehouse(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore warehouses by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25365")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25365)
    def test_put_restore_warehouses_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_wh2 = self.api_wh_warehouses.post_add_warehouses()
        model_wh3 = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_wh[0].result[0],
            model_wh2[0].result[0],
            model_wh3[0].result[0]
        )
        self.api_wh_warehouses.put_restore_warehouses_by_list(
            model_wh[0].result[0],
            model_wh2[0].result[0],
            model_wh3[0].result[0]
        )
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_wh[0].result[0],
            model_wh2[0].result[0],
            model_wh3[0].result[0]
        )

    @allure.title('Test restore warehouses by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25366")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25366)
    def test_put_restore_warehouses_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.put_restore_warehouses_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test update a non-existent warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25375")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25375)
    def test_put_update_non_existent_warehouse(self):
        self.api_wh_warehouses.put_update_non_existent_warehouse()

    @allure.title('Test update warehouse without ID field.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25376")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25376)
    def test_put_update_warehouse_without_id_field(self):
        self.api_wh_warehouses.put_update_warehouse_without_id_field()

    @allure.title('Test update deleted warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25377")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25377)
    def test_put_update_deleted_warehouse(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.put_update_deleted_warehouse(model_wh[0].result[0])

    @allure.title('Test get warehouse a non-existent ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25379")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25379)
    def test_get_non_existent_warehouses(self):
        self.api_wh_warehouses.get_non_existent_warehouses()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25381")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25381)
    @pytest.mark.parametrize('value, status_code', Params.params_negative_get_warehouse_body.value)
    def test_get_warehouse_with_negative_values(self, value, status_code, request):
        allure.dynamic.title(f"Test get a warehouse with negative values instead of ID - {request.node.callspec.id}")
        self.api_wh_warehouses.get_warehouse_with_negative_values(value, status_code)

    @allure.title('Test delete default warehouse by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25415")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25415)
    def test_delete_default_warehouse_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_default_warehouse()
        self.api_wh_warehouses.delete_default_warehouse_by_id(model_wh.result[0])
        self.api_wh_warehouses.put_update_warehouse(model_wh.result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh.result[0])

    @allure.title('Test delete deleted warehouse by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25416")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25416)
    def test_delete_deleted_warehouse_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_deleted_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete warehouses by list (undeleted, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25417")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25417)
    def test_delete_warehouses_by_list_undeleted_deleted(self):
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])
        self.api_wh_warehouses.delete_warehouses_by_list_undeleted_deleted(
            model_wh.result[0],
            model_wh.result[1]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])

    @allure.title('Test delete warehouses by list (default, undeleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25418")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25418)
    def test_delete_warehouses_by_list_default_undeleted(self):
        model_default_wh = self.api_wh_warehouses.post_add_default_warehouse()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouses_by_list_default_undeleted(
            model_default_wh.result[0],
            model_wh[0].result[0]
        )
        self.api_wh_warehouses.put_update_warehouse(model_default_wh.result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(
            model_default_wh.result[0],
            model_wh[0].result[0]
        )

    @allure.title('Test delete warehouses by list (default, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25419")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25419)
    def test_delete_warehouses_by_list_default_deleted(self):
        model_default_wh = self.api_wh_warehouses.post_add_default_warehouse()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouses_by_list_default_deleted(
            model_default_wh.result[0],
            model_wh[0].result[0],
        )
        self.api_wh_warehouses.put_update_warehouse(model_default_wh.result[0])
        self.api_wh_warehouses.delete_warehouse_by_id(model_default_wh.result[0])

    @allure.title('Test PUT restore undeleted warehouse by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25420")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25420)
    def test_put_restore_undeleted_warehouses_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.put_restore_undeleted_warehouses_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test PUT restore nonexistent warehouse by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25421")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25421)
    def test_put_restore_nonexistent_warehouses_by_id(self):
        self.api_wh_warehouses.put_restore_nonexistent_warehouses_by_id()

    @allure.title('Test PUT restore warehouses by list (undeleted, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25422")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25422)
    def test_put_restore_warehouses_by_list_undeleted_deleted(self):
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])
        self.api_wh_warehouses.put_restore_warehouses_by_list_undeleted_deleted(
            model_wh.result[0],
            model_wh.result[1]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])

    @allure.title('Test PUT restore warehouses by list (undeleted, nonexistent).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25423")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25423)
    def test_put_restore_warehouses_by_list_undeleted_nonexistent(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.put_restore_warehouses_by_list_undeleted_nonexistent(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test PUT restore warehouses by list (deleted, nonexistent).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25424")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25424)
    def test_put_restore_warehouses_by_list_deleted_nonexistent(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.put_restore_warehouses_by_list_deleted_nonexistent(model_wh[0].result[0])

    @allure.title('Test add many users to warehouse, by warehouses ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26226")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26226)
    def test_post_add_many_users_to_warehouse_by_warehouses_id(self):
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
            model_wh[0].result[0],
            model_stuff.userID
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_stuff.userID)

    @allure.title('Test add 30 users to warehouse, by warehouses ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_30_users_to_warehouse_by_list_id(self):
        list_stuff_users = self.api_adm_users.post_create_multiple_staff_users(30)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.post_add_many_users_to_warehouse_by_list_id(
            model_wh[0].result[0],
            list_stuff_users
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_many_users_by_list(list_stuff_users)

    @allure.title('Test add all stuff users to warehouse, by warehouses ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_all_stuff_users_to_warehouse(self):
        list_stuff_users = self.api_adm_users.post_create_multiple_staff_users(30)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_all_stuff_users_to_warehouse(
                model_wh[0].result[0],
                list_stuff_users
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_many_users_by_list(list_stuff_users)

    @allure.title('Test add valid user to deleted from sys warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_to_deleted_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        try:
            self.api_wh_warehouses.post_add_user_to_deleted_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add deleted from sys user to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_user_to_valid_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_deleted_user_to_valid_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add deleted and valid users to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_and_valid_user_to_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_deleted_and_valid_user_to_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID, model_users2.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users2.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add deleted and non-existent users to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_and_non_existent_user_to_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_deleted_and_non_existent_user_to_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID, non_existent_user
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid, deleted and non-existent users to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_deleted_and_non_existent_user_to_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_deleted_and_non_existent_user_to_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID, non_existent_user, model_users2.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users2.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add empty list to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_empty_list_to_warehouse_by_wh_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_empty_list_to_warehouse_by_wh_id(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid, abc, null to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_abc_null_to_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_abc_null_to_warehouse_by_wh_id(
                model_wh[0].result[0], "abc", None
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid user to already added warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_user_to_already_added_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0], model_users.userID
            )
            self.api_wh_warehouses.post_add_valid_user_to_already_added_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid user to unavailable warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_user_to_unavailable_warehouse_by_wh_id(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_warehouses.post_add_valid_user_to_unavailable_warehouse_by_wh_id(
            token_power_user_with_tenant_member_id(tenant_member_id),
            model_wh[0].result[0],
            model_registration.userID
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_registration.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add unavailable user to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_unavailable_user_to_valid_warehouse_by_wh_id(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        self.api_adm_role_permissions_ext.post_role_permissions_ext(model_role.results[0], 47)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_warehouses.post_add_unavailable_user_to_valid_warehouse_by_wh_id(
            token_power_user_with_tenant_member_id(tenant_member_id),
            model_wh[0].result[0],
            model_stuff.userID
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_users_by_list(model_registration.userID, model_stuff.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add valid user to non-existent warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_user_to_non_existent_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        non_existent_wh = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        try:
            self.api_wh_warehouses.post_add_valid_user_to_non_existent_warehouse_by_wh_id(
                non_existent_wh, model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add non-existent user to valid warehouse, by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_non_existent_user_to_valid_warehouse_by_wh_id(self):
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_non_existent_user_to_valid_warehouse_by_wh_id(
                model_wh[0].result[0], non_existent_user
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid user to valid warehouse, without token.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_to_warehouse_without_token(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_user_to_warehouse_without_token(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid users to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_users_to_valid_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid users to deleted warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_users_to_deleted_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        try:
            self.api_wh_warehouses.post_add_valid_users_to_deleted_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add 20 users to 50 warehouses, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_20_users_to_50_warehouse_by_list(self):
        list_stuff = self.api_adm_users.post_create_multiple_staff_users()
        list_warehouses = self.api_wh_warehouses.post_add_multiple_warehouses(50)
        self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
            list_warehouses,
            [list_stuff for _ in range(len(list_warehouses))]
        )
        self.api_adm_users.delete_many_users_by_list(list_stuff)
        self.api_wh_warehouses.delete_list_warehouses(list_warehouses)

    @allure.title('Test add valid users to valid warehouse, without token, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_to_warehouse_without_token_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_user_to_warehouse_without_token_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add all users to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_all_users_to_warehouse_by_list(self):
        list_users_ids = self.api_adm_users.post_create_multiple_staff_users(10)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_all_users_to_warehouse_by_list(
                model_wh[0].result[0], list_users_ids
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_many_users_by_list(list_users_ids)

    @allure.title('Test add all users with user ID to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_all_users_with_user_id_to_warehouse_by_list(self):
        list_users_ids = self.api_adm_users.post_create_multiple_staff_users(10)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_all_users_with_user_id_to_warehouse_by_list(
                model_wh[0].result[0], list_users_ids
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_many_users_by_list(list_users_ids)

    @allure.title('Test add deleted users to vali warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_deleted_user_to_valid_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        try:
            self.api_wh_warehouses.post_add_deleted_user_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid user to non-existent warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_to_non_existent_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        non_existent_wh = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        try:
            self.api_wh_warehouses.post_add_user_to_non_existent_warehouse_by_list(
                [non_existent_wh], [[model_users.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add non-existent user to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_non_existent_user_to_valid_warehouse_by_list(self):
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_non_existent_user_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[non_existent_user]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid and deleted from sys user to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_and_deleted_user_to_valid_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users2.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_and_deleted_user_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID, model_users2.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add valid and non-existent user to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_and_non_existent_user_to_valid_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_and_non_existent_user_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID, non_existent_user]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add valid user to valid and deleted warehouses, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_user_to_valid_and_deleted_warehouses_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[1])
        try:
            self.api_wh_warehouses.post_add_valid_user_to_valid_and_deleted_warehouses_by_list(
                [model_wh.result[0], model_wh.result[1]],
                [[model_users.userID, model_users2.userID], [model_users.userID, model_users2.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh.result[0])
            self.api_adm_users.delete_users_by_list(model_users.userID, model_users2.userID)

    @allure.title('Test add valid user to valid and non-existent warehouses, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_user_to_valid_and_non_existent_warehouses_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        non_existent_wh = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        try:
            self.api_wh_warehouses.post_add_valid_user_to_valid_and_non_existent_warehouses_by_list(
                [model_wh[0].result[0], non_existent_wh],
                [[model_users.userID, model_users2.userID], [model_users.userID, model_users2.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_users_by_list(model_users.userID, model_users2.userID)

    @allure.title('Test add valid user to null warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_valid_user_to_warehouse_null_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        try:
            self.api_wh_warehouses.post_add_valid_user_to_warehouse_null_by_list(
                [None],
                [[model_users.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add empty list users to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_empty_list_users_to_warehouse_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_empty_list_users_to_warehouse_by_list(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add null users to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_null_user_to_warehouse_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_null_user_to_warehouse_by_list(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test add valid user to already added warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_to_already_added_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
            self.api_wh_warehouses.post_add_user_to_already_added_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )

        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test add valid user to unavailable warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_user_to_unavailable_warehouse_by_list(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_warehouses.post_add_user_to_unavailable_warehouse_by_list(
            token_power_user_with_tenant_member_id(tenant_member_id),
            [model_wh[0].result[0]],
            [[model_registration.userID]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_user_by_id(model_registration.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test add unavailable user to valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_add_unavailable_user_to_valid_warehouse_by_list(self, token_power_user_with_tenant_member_id):
        list_app = self.api_common_applications.get_and_return_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_applications.post_add_list_role_applications(model_role.results[0], list_app)
        self.api_adm_role_permissions_ext.post_role_permissions_ext(model_role.results[0], 47)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_stuff = self.api_adm_users.post_add_user_staff()
        model_template = self.api_adm_user_templates.post_add_user_template()
        model_invitation = self.api_adm_invitations.post_add_invitation(model_template.results[0])
        model_registration = self.api_adm_users.post_add_users_registration(model_invitation.results[0].id)
        self.api_adm_users.post_add_users_registration_verify(model_registration.accountID)
        self.api_adm_users.post_change_to_stuff_users(model_registration.userID)
        self.api_adm_user_roles.post_add_roles_to_user(
            model_registration.userID,
            model_role.results[0]
        )
        tenant_member_id = self.api_adm_tenant_members.get_list_tenant_members_return_tenant_member_id(
            model_registration.userID
        )
        self.api_wh_warehouses.post_add_unavailable_user_to_valid_warehouse_by_list(
            token_power_user_with_tenant_member_id(tenant_member_id),
            [model_wh[0].result[0]],
            [[model_stuff.userID]]
        )
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_adm_users.delete_users_by_list(model_registration.userID, model_stuff.userID)
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
        self.api_adm_invitations.delete_invitations_by_list(model_invitation.results[0].id)
        self.api_adm_user_templates.delete_user_template_by_id(model_template.results[0])

    @allure.title('Test delete user from warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
            self.api_wh_warehouses.delete_users_from_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete user from already deleted warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_already_deleted_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
                [model_wh[0].result[0]], [[model_users.userID]]
            )
            self.api_wh_warehouses.delete_users_from_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_already_deleted_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete user from non-existent warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_user_from_non_existent_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        non_existent_wh = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        try:
            self.api_wh_warehouses.delete_user_from_non_existent_warehouse_by_wh_id(
                non_existent_wh, model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete non-existent user from warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_non_existent_user_from_valid_warehouse_by_wh_id(self):
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_non_existent_user_from_valid_warehouse_by_wh_id(
                model_wh[0].result[0], non_existent_user
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete empty list users from valid warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_empty_list_users_from_warehouse_by_wh_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_empty_list_users_from_warehouse_by_wh_id(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete users=null from valid warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_null_from_warehouse_by_wh_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_null_from_warehouse_by_wh_id(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete valid user from deleted from sys warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_user_from_deleted_from_sys_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        try:
            self.api_wh_warehouses.delete_valid_user_from_deleted_from_sys_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete deleted from sys user from valid warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_deleted_user_from_valid_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        try:
            self.api_wh_warehouses.delete_deleted_user_from_valid_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete 30 user from valid warehouse by warehouse ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_30_users_from_valid_warehouse_by_wh_id(self):
        list_stuff_users = self.api_adm_users.post_create_multiple_staff_users(30)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_list_id(
                model_wh[0].result[0],
                list_stuff_users
            )
            self.api_wh_warehouses.delete_list_users_from_warehouse_by_wh_id(
                model_wh[0].result[0], list_stuff_users
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_many_users_by_list(list_stuff_users)

    @allure.title('Test delete all users from valid warehouse by warehouse ID. isRelatedToAnyUser=true.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_all_users_from_valid_warehouse_by_wh_id(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_all_users_from_valid_warehouse_by_wh_id(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete valid user from valid warehouse by warehouse ID, without authorization.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_warehouse_without_authorization(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_warehouse_without_authorization(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete all users from valid warehouse, Warehouses/users. isRelatedToAnyUser=true.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_all_users_from_valid_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_all_users_from_valid_warehouse_by_list(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete valid user from valid warehouse, Warehouses/users, without authorization.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_warehouse_by_list_without_authorization(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_warehouse_by_list_without_authorization(
                model_wh[0].result[0], model_users.userID
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete 20 users from 100 warehouses, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_20_users_from_100_warehouse_by_list(self):
        list_users = self.api_adm_users.post_create_multiple_staff_users()
        list_wh = self.api_wh_warehouses.post_add_multiple_warehouses(100)
        try:
            self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
                list_wh,
                [list_users for _ in range(len(list_wh))]
            )
            self.api_wh_warehouses.delete_users_from_valid_warehouses_by_list(
                list_wh,
                [list_users for _ in range(len(list_wh))]
            )
        finally:
            self.api_wh_warehouses.delete_list_warehouses(list_wh)
            self.api_adm_users.delete_many_users_by_list(list_users)

    @allure.title('Test delete valid user from already deleted warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_already_deleted_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_already_deleted_warehouse_by_list(
                [model_wh[0].result[0]],
                [[model_users.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete valid user from already deleted warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_already_deleted_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_many_users_to_warehouse_by_warehouses_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_warehouse_by_wh_id(
                model_wh[0].result[0],
                model_users.userID
            )
            self.api_wh_warehouses.delete_users_from_already_deleted_warehouse_by_list(
                [model_wh[0].result[0]],
                [[model_users.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete valid user from non-existent warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_from_non_existent_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        non_existent_wh = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        try:
            self.api_wh_warehouses.delete_users_from_non_existent_warehouse_by_list(
                [non_existent_wh],
                [[model_users.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete non-existent user from warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_non_existent_users_from_warehouse_by_list(self):
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_non_existent_users_from_warehouse_by_list(
                [model_wh[0].result[0]],
                [[non_existent_user]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete valid, deleted, non-existent users from warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_non_existent_deleted_users_from_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users2.userID)
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_valid_non_existent_deleted_users_from_warehouse_by_list(
                [model_wh[0].result[0]],
                [[model_users.userID, non_existent_user, model_users2.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete deleted, non-existent users from deleted warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_non_existent_deleted_users_from_deleted_warehouse_by_list(self):
        model_users2 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users2.userID)
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_warehouses.delete_non_existent_deleted_users_from_deleted_warehouse_by_list(
            [model_wh[0].result[0]],
            [[non_existent_user, model_users2.userID]]
        )

    @allure.title('Test delete (deleted, non-existent), (valid) users from valid warehouses, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_non_existent_deleted_and_valid_users_from_warehouses_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_users2 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users2.userID)
        non_existent_user = self.api_adm_users.get_non_existent_user_id()
        model_wh = self.api_wh_warehouses.post_add_two_warehouses()
        try:
            self.api_wh_warehouses.delete_non_existent_deleted_and_valid_users_from_warehouses_by_list(
                model_wh.result,
                [[model_users.userID], [non_existent_user, model_users2.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_list_warehouses(model_wh.result)

    @allure.title('Test delete valid users from deleted from sys warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_users_from_deleted_from_sys_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        try:
            self.api_wh_warehouses.delete_valid_users_from_deleted_from_sys_warehouse_by_list(
                model_wh[0].result,
                [[model_users.userID]]
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete deleted from sys users from valid warehouse, Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_deleted_from_sys_user_from_valid_warehouse_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_users.userID)
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_deleted_from_sys_user_from_valid_warehouse_by_list(
                model_wh[0].result,
                [[model_users.userID]]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete valid user from warehouse=null. Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_valid_user_from_warehouse_null_by_list(self):
        model_users = self.api_adm_users.post_add_user_staff()
        try:
            self.api_wh_warehouses.delete_valid_user_from_warehouse_null_by_list(
                model_users.userID
            )
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)

    @allure.title('Test delete empty list users from valid warehouse. Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_empty_list_users_from_valid_warehouse_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_empty_list_users_from_valid_warehouse_by_list(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test delete user=null from valid warehouse. Warehouses/users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_user_is_null_from_valid_warehouse_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.delete_user_is_null_from_valid_warehouse_by_list(
                model_wh[0].result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test get list stuff users added to warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_stuff_users_added_to_warehouse(self):
        model_users = self.api_adm_users.post_add_user_staff()
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            self.api_wh_warehouses.post_add_valid_users_to_valid_warehouse_by_list(
                model_wh[0].result,
                [[model_users.userID]]
            )
            model_users_added_warehouse = self.api_wh_warehouses.get_list_stuff_users_added_to_warehouse(
                model_wh[0].result[0]
            )
            assert model_users_added_warehouse.results[0].userID == model_users.userID, \
                f"Invalid list of users added to the warehouse was received."
        finally:
            self.api_adm_users.delete_user_by_id(model_users.userID)
            self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])

    @allure.title('Test get list of users of the non-existent warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_users_of_non_existent_warehouse(self):
        non_existent_wh = self.api_wh_warehouses.get_non_existent_warehouse_return_id()
        self.api_wh_warehouses.get_list_users_of_non_existent_warehouse(non_existent_wh)

    @allure.title('Test get checking that no users have been added to the warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_no_users_added_to_warehouse(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.get_no_users_added_to_warehouse(model_wh[0].result[0])
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
