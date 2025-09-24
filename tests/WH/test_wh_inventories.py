import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWhInventories(BaseTest):

    # @allure.title('Test add inventories.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24508")
    # @pytest.mark.regress
    # @pytest.mark.skip(reason="Тест на добавления инвентаризации проходит в - test_delete_inventories_by_list")
    # @pytest.mark.test_case_id(24508)
    # def test_post_add_inventories(self):
    #     model_wh = self.api_wh_warehouses.post_add_warehouses()
    #     model_materials = self.api_wh_materials.post_add_materials()
    #     wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
    #     materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
    #     self.api_wh_inventories.post_add_inventories(
    #         materials_data.erpID,
    #         materials_data.name,
    #         wh_data.erpID,
    #         wh_data.name,
    #     )

    @allure.title('Test delete inventories by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24509")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24509)
    def test_delete_inventories_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_materials = self.api_wh_materials.post_add_materials()
        wh_data = self.api_wh_warehouses.get_warehouses_by_id(model_wh[0].result[0])
        materials_data = self.api_wh_materials.get_material_by_id(model_materials.result[0])
        model_inventories = self.api_wh_inventories.post_add_inventories(
            materials_data.erpID,
            materials_data.name,
            wh_data.erpID,
            wh_data.name
        )
        self.api_wh_inventories.delete_inventories_by_list(model_inventories.result[0].id)
