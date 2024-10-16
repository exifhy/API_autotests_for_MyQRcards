import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Managing enterprise structure")
class TestEsAssetClasses(BaseTest):

    @allure.title('Test add asset class.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23598")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23598)
    @pytest.mark.skip(reason='Asset class is created in test - test_delete_asset_classes_by_id.')
    def test_post_add_asset_class(self):
        self.api_es_asset_classes.post_add_asset_class()

    @allure.title('Test delete asset class by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23603")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23603)
    def test_delete_asset_classes_by_id(self):
        asset_class_id, name_asset_class = self.api_es_asset_classes.post_add_asset_class()
        self.api_es_asset_classes.delete_asset_classes_by_id(asset_class_id=asset_class_id.list[0].id)

    @allure.title('Test delete mass asset class.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23601")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23601)
    def test_delete_mass_asset_classes(self):
        first_asset_class_id, first_name_asset_class = self.api_es_asset_classes.post_add_asset_class()
        second_asset_class_id, second_name_asset_class = self.api_es_asset_classes.post_add_asset_class()
        asset_classes_id = {first_asset_class_id.list[0].id, second_asset_class_id.list[0].id}
        self.api_es_asset_classes.delete_mass_asset_classes(*asset_classes_id)

    @allure.title('Test get list asset class.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23599")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23599)
    def test_get_list_asset_classes_by_id(self):
        self.api_es_asset_classes.get_list_asset_classes()

    @allure.title('Test get list asset class.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23602")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23602)
    def test_get_asset_classes_by_id(self):
        asset_class_id, name_asset_class = self.api_es_asset_classes.post_add_asset_class()
        model_asset_class = self.api_es_asset_classes.get_asset_classes_by_id(asset_class_id.list[0].id)
        assert model_asset_class.name == name_asset_class, \
            f'Expected <{name_asset_class}>, but got <{model_asset_class.name}>.'
        self.api_es_asset_classes.delete_asset_classes_by_id(asset_class_id.list[0].id)

    @allure.title('Test update asset class.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23600")
    @pytest.mark.regress
    @pytest.mark.test_case_id(236000)
    def test_put_update_asset_class(self):
        asset_class_id, name_asset_class = self.api_es_asset_classes.post_add_asset_class()
        self.api_es_asset_classes.put_update_asset_class(asset_class_id.list[0].id)
        model_asset_class = self.api_es_asset_classes.get_asset_classes_by_id(asset_class_id.list[0].id)
        assert model_asset_class.name != name_asset_class, \
            f'Expected <{name_asset_class}>, but got <{model_asset_class.name}>.'
        self.api_es_asset_classes.delete_asset_classes_by_id(asset_class_id.list[0].id)
