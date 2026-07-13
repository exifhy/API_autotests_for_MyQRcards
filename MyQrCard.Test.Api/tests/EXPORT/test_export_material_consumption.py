import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export material consumption data")
class TestExportMaterialConsumption(BaseTest):

    @allure.title('Test exports the list of material consumption(template).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23208")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23208)
    def test_get_export_list_material_costs_template(self):
        self.api_export_material_consumption.get_export_list_material_costs()
