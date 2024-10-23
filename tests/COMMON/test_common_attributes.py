import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries")
class TestCommonAttributes(BaseTest):

    @allure.title('Test attribute creation method for contract only.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23548")
    @pytest.mark.skip(reason='Тест на создание атрибута для договора есть в тесте ')
    @pytest.mark.regress
    @pytest.mark.test_case_id(23548)
    def test_post_add_method_attributes_only_for_contract(self):
        self.api_common_attributes.post_add_method_attributes_only_for_contract()

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
