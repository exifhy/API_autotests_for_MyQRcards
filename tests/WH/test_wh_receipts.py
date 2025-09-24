import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
@pytest.mark.xdist_group(name="many_users")
class TestWhReceipts(BaseTest):

    # @allure.title('Test add receipts.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24499")
    # @pytest.mark.regress
    # @pytest.mark.skip(reason="Тест на оприходование проходит в - test_delete_receipts_by_list")
    # @pytest.mark.test_case_id(24499)
    # def test_post_add_receipts(self):
    #     model_wh = self.api_wh_warehouses.post_add_warehouses()
    #     self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])

    @allure.title('Test delete receipts by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24502")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24502)
    def test_delete_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipts = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipts_by_list(model_receipts.result[0])
        self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    # @allure.title('Test add items receipts.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24500")
    # @pytest.mark.regress
    # @pytest.mark.skip(reason="Тест на оприходование проходит в - test_delete_items_receipts")
    # @pytest.mark.test_case_id(24500)
    # def test_post_add_items_receipts(self):
    #     model_wh = self.api_wh_warehouses.post_add_warehouses()
    #     materials = self.api_wh_materials.post_add_materials()
    #     model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
    #     try:
    #         self.api_wh_receipts.post_add_items_receipts(
    #             model_receipt.result[0],
    #             materials.result[0],
    #         )
    #     finally:
    #         self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
    #         self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
    #         self.api_wh_materials.delete_materials_by_list(materials.result[0])

    @allure.title('Test delete items receipts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24503")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24503)
    def test_delete_items_receipts(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        materials = self.api_wh_materials.post_add_materials()
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

    @allure.title('Test delete item receipt by material ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25558")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25558)
    def test_delete_item_receipt_by_material_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        materials = self.api_wh_materials.post_add_materials()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.post_add_items_receipts(
                model_receipt.result[0],
                materials.result[0],
            )
            self.api_wh_receipts.delete_item_receipt_by_material_id(
                model_receipt.result[0],
                materials.result[0]
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
            self.api_wh_materials.delete_materials_by_list(materials.result[0])

    @allure.title('Test get nonexistent receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25556")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25556)
    def test_get_nonexistent_receipt_by_id(self):
        self.api_wh_receipts.get_nonexistent_receipt_by_id()

    @allure.title('Test get receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25539")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25539)
    def test_get_receipt_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.get_receipt_by_id(
                model_receipt.result[0]
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test delete deleted receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25546")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25546)
    def test_delete_deleted_receipt_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
        try:
            self.api_wh_receipts.delete_deleted_receipt_by_id(
                model_receipt.result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test delete nonexistent receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25547")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25547)
    def test_delete_nonexistent_receipt_by_id(self):
        self.api_wh_receipts.delete_nonexistent_receipt_by_id()

    @allure.title('Test delete receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25541")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25541)
    def test_delete_receipt_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.delete_receipt_by_id(
                model_receipt.result[0]
            )
        finally:
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test get list receipts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25548")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25548)
    def test_get_list_receipts(self):
        self.api_wh_receipts.get_list_receipts()

    @allure.title('Test get list receipts with range.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25560")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25560)
    def test_get_list_receipts_with_range(self):
        self.api_wh_receipts.get_list_receipts_with_range()

    @allure.title('Test head receipts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25549")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25549)
    def test_head_receipts(self):
        self.api_wh_receipts.head_receipts()

    @allure.title('Test update receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25561")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25561)
    def test_put_update_receipts(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_wh2 = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.put_update_receipts(
                model_receipt.result[0],
                model_wh2[0].result[0],
                model_wh2[1]
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore receipts by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25562")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25562)
    def test_put_restore_receipts_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipt_by_id(model_receipt.result[0])
        try:
            self.api_wh_receipts.put_restore_receipts_by_id(model_receipt.result[0])
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore undeleted receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25564")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25564)
    def test_put_restore_undeleted_receipts_by_id(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.put_restore_undeleted_receipts_by_id(model_receipt.result[0])
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore nonexistent receipt by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25565")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25565)
    def test_put_restore_nonexistent_receipts_by_id(self):
        self.api_wh_receipts.put_restore_nonexistent_receipts_by_id()

    @allure.title('Test restore receipts by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25567")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25567)
    def test_put_restore_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_three_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipts_by_list(
            model_receipt.result[0],
            model_receipt.result[1],
            model_receipt.result[2],
        )
        try:
            self.api_wh_receipts.put_restore_receipts_by_list(
                model_receipt.result[0],
                model_receipt.result[1],
                model_receipt.result[2]
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(
                model_receipt.result[0],
                model_receipt.result[1],
                model_receipt.result[2],
            )
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore receipts by list (undeleted, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25569")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25569)
    def test_put_restore_undeleted_deleted_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_two_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipt_by_id(model_receipt.result[1])
        try:
            self.api_wh_receipts.put_restore_undeleted_deleted_receipts_by_list(
                model_receipt.result[0],
                model_receipt.result[1]
            )
        finally:
            self.api_wh_receipts.delete_receipt_by_id(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore receipts by list (undeleted, undeleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25570")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25570)
    def test_put_restore_undeleted_undeleted_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_two_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.put_restore_undeleted_undeleted_receipts_by_list(
                model_receipt.result[0],
                model_receipt.result[1]
            )
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0], model_receipt.result[1])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore receipts by list (nonexistent, undeleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25571")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25571)
    def test_put_restore_nonexistent_undeleted_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.put_restore_nonexistent_undeleted_receipts_by_list(model_receipt.result[0])
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test restore receipts by list (nonexistent, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25573")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25573)
    def test_put_restore_nonexistent_deleted_receipts_by_list(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        self.api_wh_receipts.delete_receipt_by_id(model_receipt.result[0])
        try:
            self.api_wh_receipts.put_restore_nonexistent_deleted_receipts_by_list(model_receipt.result[0])
        finally:
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test get list receipt items by receipt ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25574")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25574)
    @pytest.mark.xfail(reason="Баг, приходит 201 вместо 200 или 206")
    def test_get_list_receipt_items(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        materials = self.api_wh_materials.post_add_materials()
        model_receipt = self.api_wh_receipts.post_add_receipts(model_wh[0].result[0], model_wh[1])
        try:
            self.api_wh_receipts.post_add_items_receipts(
                model_receipt.result[0],
                materials.result[0],
            )
            self.api_wh_receipts.get_list_receipt_items(model_receipt.result[0])
        finally:
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])
            self.api_wh_materials.delete_materials_by_list(materials.result[0])

    @allure.title('Test add receipt with deleted warehouse.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25583")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25583)
    def test_post_add_receipt_with_deleted_warehouses(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        self.api_wh_warehouses.delete_warehouse_by_id(model_wh[0].result[0])
        self.api_wh_receipts.post_add_receipt_with_deleted_warehouses(model_wh[0].result[0], model_wh[1])

    @allure.title('Test add receipt without number field.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25584")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25584)
    @pytest.mark.xfail(reason="Баг, приход создается без обязательного поля <number>")
    def test_post_add_receipt_without_number_field(self):
        model_wh = self.api_wh_warehouses.post_add_warehouses()
        try:
            model_receipt = self.api_wh_receipts.post_add_receipt_without_number_field(
                model_wh[0].result[0], model_wh[1]
            )
            self.api_wh_receipts.delete_receipts_by_list(model_receipt.result[0])
        finally:
            self.api_wh_warehouses.delete_warehouses_by_list(model_wh[0].result[0])

    @allure.title('Test add receipt without warehouseID field.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25586")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25586)
    def test_post_add_receipt_without_warehouse_id_field(self):
        self.api_wh_receipts.post_add_receipt_without_warehouse_id_field()
