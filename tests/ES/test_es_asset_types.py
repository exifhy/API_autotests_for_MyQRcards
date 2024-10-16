import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Managing enterprise structure")
class TestEsAssetTypes(BaseTest):

    @allure.title('Test add asset class.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23590")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23590)
    def test_get_list_asset_types(self):
        self.api_es_asset_types.get_list_asset_types()
