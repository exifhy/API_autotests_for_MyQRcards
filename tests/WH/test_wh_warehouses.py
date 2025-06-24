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
