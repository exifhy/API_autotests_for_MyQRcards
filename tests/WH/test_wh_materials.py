import allure
import pytest
from config.base_test import BaseTest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWhMaterials(BaseTest):

    @allure.title('Test add materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24497")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на создание материала проходит в - test_delete_materials_by_list")
    @pytest.mark.test_case_id(24497)
    def test_post_add_materials(self):
        self.api_wh_materials.post_add_materials()

    @allure.title('Test delete materials by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24498")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на удаление материала проходит в - test_get_material_by_id")
    @pytest.mark.test_case_id(24498)
    def test_delete_materials_by_list(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get material by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24507")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24507)
    def test_get_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.get_material_by_id(model_materials.result[0])
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test head materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25458")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25458)
    def test_head_materials(self):
        self.api_wh_materials.head_materials()

    @allure.title('Test add attachments to material by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25460")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25460)
    def test_post_attachments_to_material_by_list(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        self.api_wh_materials.post_attachments_to_material_by_list(
            model_materials.result[0], attachment_id.attachmentID
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get list attachments by material ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_attachments_by_material_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_wh_materials.get_list_attachments_by_material_id(model_materials.result[0])
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test delete attachments from material by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_attachments_from_material_by_list(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_wh_materials.delete_attachments_from_material_by_list(
            model_materials.result[0], attachment_id.results[0].attachmentID
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get attachment from material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_attachment_from_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_wh_materials.get_attachment_from_material_by_id(
            model_materials.result[0], attachment_id.results[0].attachmentID
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test delete attachment by ID from material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_attachment_from_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_wh_materials.delete_attachment_from_material_by_id(
            model_materials.result[0], attachment_id.results[0].attachmentID
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get TemporaryRedirect to a temporary link for downloading the attachment file from material.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_downloading_attachment_file_from_material(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_wh_materials.get_downloading_attachment_file_from_material(
            model_materials.result[0], attachment_id
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get temporary link for downloading the attachment file from material (noRedirect).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_downloading_attachment_file_from_material_no_redirect(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_wh_materials.get_downloading_attachment_file_from_material_no_redirect(
            model_materials.result[0], attachment_id.results[0].attachmentID
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test uploads the file to server and binds it to the material, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_upload_attachment_and_bind_to_material_data_from_form(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_form(
            model_materials.result[0]
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.results[0].attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test uploads the file to server and binds it to the material, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_post_upload_attachment_and_bind_to_material_data_from_body(self):
        model_materials = self.api_wh_materials.post_add_materials()
        attachment_id = self.api_wh_materials.post_upload_attachment_and_bind_to_material_data_from_body(
            model_materials.result[0]
        )
        self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test add barcodes to material.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    @pytest.mark.skip(reason="Тест на создание barcode проходит в - test_delete_barcode_from_material_by_id")
    def test_post_add_barcodes_material(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.post_add_barcodes_material(
            model_materials.result[0]
        )
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test delete barcode from material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_barcode_from_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        barcode_id = self.api_wh_materials.post_add_barcodes_material(
            model_materials.result[0]
        )
        self.api_wh_materials.delete_barcode_from_material_by_id(
            model_materials.result[0], barcode_id.results[0].id
        )
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test delete barcodes from material by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_barcodes_from_material_by_list(self):
        model_materials = self.api_wh_materials.post_add_materials()
        model_barcodes = self.api_wh_materials.post_add_two_barcodes_material(
            model_materials.result[0]
        )
        self.api_wh_materials.delete_barcodes_from_material_by_list(
            model_materials.result[0], model_barcodes.results[0].id, model_barcodes.results[1].id
        )
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get list barcodes material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_barcodes_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.post_add_barcodes_material(
            model_materials.result[0]
        )
        self.api_wh_materials.get_list_barcodes_material_by_id(model_materials.result[0])
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test update material barcode.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_update_material_barcode(self):
        model_materials = self.api_wh_materials.post_add_materials()
        model_barcode = self.api_wh_materials.post_add_barcodes_material_with_barcode_type_id(model_materials.result[0])
        self.api_wh_materials.put_update_material_barcode(model_materials.result[0], model_barcode.results[0].id)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get list materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_materials(self):
        self.api_wh_materials.get_list_materials()

    @allure.title('Test get list materials V2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_materials_v2(self):
        self.api_wh_materials.get_list_materials_v2()

    @allure.title('Test get required list materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_required_materials(self):
        self.api_wh_materials.get_list_required_materials()

    @allure.title('Test delete material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test restore materials by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_materials_by_list(self):
        model_materials = self.api_wh_materials.post_add_three_materials()
        self.api_wh_materials.delete_materials_by_list(
            model_materials.result[0],
            model_materials.result[1],
            model_materials.result[2],
        )
        self.api_wh_materials.put_restore_materials_by_list(
            model_materials.result[0],
            model_materials.result[1],
            model_materials.result[2],
        )
        self.api_wh_materials.delete_materials_by_list(
            model_materials.result[0],
            model_materials.result[1],
            model_materials.result[2],
        )

    @allure.title('Test restore materials by list (undeleted, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_materials_by_list_undeleted_deleted(self):
        model_materials = self.api_wh_materials.post_add_two_materials()
        self.api_wh_materials.delete_material_by_id(model_materials.result[1])
        self.api_wh_materials.put_restore_materials_by_list_undeleted_deleted(
            model_materials.result[0],
            model_materials.result[1]
        )
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test restore materials by list (nonexistent, undeleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_materials_by_list_nonexistent_undeleted(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.put_restore_materials_by_list_nonexistent_undeleted(model_materials.result[0])
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test restore materials by list (nonexistent, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_materials_by_list_nonexistent_deleted(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])
        self.api_wh_materials.put_restore_materials_by_list_nonexistent_deleted(model_materials.result[0])

    @allure.title('Test restore materials by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_material_by_id(self):
        model_material = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.delete_material_by_id(model_material.result[0])
        self.api_wh_materials.put_restore_material_by_id(model_material.result[0])
        self.api_wh_materials.delete_material_by_id(model_material.result[0])

    @allure.title('Test restore undeleted material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_undeleted_material_by_id(self):
        model_material = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.put_restore_undeleted_material_by_id(model_material.result[0])
        self.api_wh_materials.delete_material_by_id(model_material.result[0])

    @allure.title('Test restore nonexistent material by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_put_restore_nonexistent_material_by_id(self):
        self.api_wh_materials.put_restore_nonexistent_material_by_id()

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    @pytest.mark.parametrize('data, name_step, error_message', Params.params_negative_add_materials_body.value)
    def test_post_add_material_negative(self, data, name_step, error_message, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        self.api_wh_materials.post_add_material_negative(data, name_step, error_message)

    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    @pytest.mark.parametrize('data, name_step, error_message', Params.params_negative_update_material_body.value)
    def test_put_update_material_negative(self, data, name_step, error_message, request):
        allure.dynamic.title(f"{request.node.callspec.id}")
        model_material = self.api_wh_materials.post_add_materials()
        try:
            self.api_wh_materials.put_update_material_negative(
                model_material.result[0], data, name_step, error_message
            )
        finally:
            self.api_wh_materials.delete_material_by_id(model_material.result[0])

    @allure.title('Test add barcodes to material with nonexistent barcodeTypeID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    @pytest.mark.skip(reason="Ручка в разработке, создается штрихкод с несуществующем типом.")
    def test_post_add_barcodes_material_with_nonexistent_barcode_type_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        try:
            self.api_wh_materials.post_add_barcodes_material_with_nonexistent_barcode_type_id(
                model_materials.result[0]
            )
        finally:
            self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test add barcodes to material with empty string in value.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    @pytest.mark.skip(reason="Ручка в разработке, создается штрих код с пустым значением в value.")
    def test_post_add_barcodes_material_with_empty_string_in_value(self):
        model_materials = self.api_wh_materials.post_add_materials()
        try:
            self.api_wh_materials.post_add_barcodes_material_with_empty_string_in_value(
                model_materials.result[0]
            )
        finally:
            self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test delete materials by list (undeleted, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_materials_by_list_undeleted_deleted(self):
        model_materials = self.api_wh_materials.post_add_two_materials()
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])
        try:

            self.api_wh_materials.delete_materials_by_list_negative_already_done(
                model_materials.result[0],
                model_materials.result[1]
            )
        finally:
            self.api_wh_materials.delete_material_by_id(model_materials.result[1])

    @allure.title('Test delete materials by list (deleted, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_materials_by_list_deleted_deleted(self):
        model_materials = self.api_wh_materials.post_add_two_materials()
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0], model_materials.result[1])
        self.api_wh_materials.delete_materials_by_list_negative_already_done(
            model_materials.result[0],
            model_materials.result[1]
        )

    @allure.title('Test delete materials by list (nonexistent, deleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_materials_by_list_nonexistent_deleted(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])
        self.api_wh_materials.delete_materials_by_list_negative_not_found(model_materials.result[0])

    @allure.title('Test delete materials by list (nonexistent, undeleted).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_materials_by_list_nonexistent_undeleted(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.delete_materials_by_list_negative_not_found(model_materials.result[0])
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test get list materials V2 (isDeleted=true).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_deleted_materials_v2(self):
        self.api_wh_materials.get_list_deleted_materials_v2()

    @allure.title('Test get list materials V2 (isDeleted=false).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_undeleted_materials_v2(self):
        self.api_wh_materials.get_list_undeleted_materials_v2()

    @allure.title('Test get list materials, searchText={POST WH/materials name}.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_materials_search_text_new_material(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.get_list_materials_search_text_new_material(model_materials.result[0])
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])

    @allure.title('Test get list materials, searchText={POST WH/materials erpID}.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_get_list_materials_search_text_erp_id(self):
        model_materials = self.api_wh_materials.post_add_materials()
        self.api_wh_materials.get_list_materials_search_text_erp_id(model_materials.result[0])
        self.api_wh_materials.delete_material_by_id(model_materials.result[0])
