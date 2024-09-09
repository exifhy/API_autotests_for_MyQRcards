import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export materials data")
class TestExportMaterials(BaseTest):

    @allure.title('Test exports the list of materials(template).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23207")
    @pytest.mark.smoke
    def test_get_export_list_materials(self):
        self.api_export_materials.get_export_list_materials()
