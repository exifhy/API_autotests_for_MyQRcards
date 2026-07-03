import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonAttributes(BaseTest):

    # @allure.title('Test attribute creation method for contract only.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23548")
    # @pytest.mark.skip(reason='Тест на создание атрибута для договора есть в тесте - test_delete_attribute_by_id')
    # @pytest.mark.test_case_id(23548)
    # def test_post_add_method_attributes_only_for_contract(self):
    #     self.api_common_attributes.post_add_method_attributes_only_for_contract()

    @allure.title('Test delete attribute by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23549")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23549)
    def test_delete_attribute_by_id(self):
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_contract()
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test get available values for an attribute.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23640")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23640)
    def test_get_available_values_for_attribute(self):
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_all_relevant_essence_with_type_6()
        values = self.api_common_attribute_list_of_values.post_add_attribute_list_of_value_with_five_fields(
            attribute_id=attribute_id.values[0]
        )
        try:
            result = self.api_common_attributes.get_available_values_for_attribute(
                attribute_id=attribute_id.values[0]
            )
            assert values == result[1], f'Expected <{values}>, but got <{result[1]}>'
        finally:
            self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test attribute creation method for customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26868")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26868)
    def test_post_add_attribute_only_for_customer(self):
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_customer()
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test attribute creation method for stuff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26867")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26867)
    def test_post_add_attribute_only_for_stuff(self):
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test attribute creation method for stuff and customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26866")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26866)
    def test_post_add_attribute_for_stuff_and_customer(self):
        attribute_id = self.api_common_attributes.post_add_attribute_for_stuff_and_customer()
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test attribute creation method stuff false and customer false.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26869")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26869)
    def test_post_add_attribute_stuff_and_customer_false(self):
        attribute_id = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test get list attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26870")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26870)
    def test_get_list_attributes(self):
        self.api_common_attributes.get_list_attributes()

    @allure.title('Test put users attribute update method.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26872")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26872)
    def test_put_update_users_attribute(self):
        attribute_id = self.api_common_attributes.post_add_attribute_for_stuff_and_customer()
        self.api_common_attributes.put_update_users_attribute(
            attribute_id.values[0], False, False
        )
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test get attribute by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26873")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26873)
    def test_get_attribute_by_id(self):
        attribute_id = self.api_common_attributes.post_add_attribute_only_for_stuff()
        self.api_common_attributes.get_attribute_by_id(attribute_id=attribute_id.values[0])
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title('Test delete mass attributes by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/26871")
    @pytest.mark.regress
    @pytest.mark.test_case_id(26871)
    def test_delete_attributes_by_list(self):
        attribute_first = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        attribute_second = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        attribute_third = self.api_common_attributes.post_add_attribute_stuff_and_customer_false()
        self.api_common_attributes.delete_attributes_by_list(
            attribute_first.values[0],
            attribute_second.values[0],
            attribute_third.values[0],
        )
