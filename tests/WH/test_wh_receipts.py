import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWhReceipts(BaseTest):

    @allure.title('Test add receipts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24499")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на оприходование проходит в - test_delete_receipts_by_list")
    @pytest.mark.test_case_id(24499)
    def test_post_add_receipts(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])

    @allure.title('Test delete receipts by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24502")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24502)
    def test_delete_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipts = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipts_by_list(model_receipts.result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test add items receipts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24500")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на оприходование проходит в - test_delete_items_receipts")
    @pytest.mark.test_case_id(24500)
    def test_post_add_items_receipts(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        materials = self.api_wh_materials.post_add_materials(model_wh[1])
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.post_add_items_receipts(
                model_receipt.result[0],
                materials.result[0],
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
            self.api_wh_materials.delete_materials_by_list(materials.result[0])

    @allure.title('Test delete items receipts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24503")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24503)
    def test_delete_items_receipts(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        materials = self.api_wh_materials.post_add_materials(model_wh[1])
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.post_add_items_receipts(
                model_receipt.result[0],
                materials.result[0],
            )
            self.api_wh_receipts.delete_items_receipts_by_list(
                model_receipt.result[0],
                materials.result[0]
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
            self.api_wh_materials.delete_materials_by_list(materials.result[0])
