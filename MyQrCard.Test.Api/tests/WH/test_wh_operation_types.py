import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service offers application programming interface for warehouses.")
class TestWhOperationTypes(BaseTest):

    @allure.title('Test get operation type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28837")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28837)
    def test_get_operation_type_by_id(self):
        model_doc_type = self.api_wh_document_types.get_document_types()
        model_operation_type = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        self.api_wh_operation_types.get_operation_type_by_id(model_operation_type.results[0].id)
        self.api_wh_operation_types.delete_operation_type_by_id(model_operation_type.results[0].id)

    @allure.title('Test delete operation type by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28838")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28838)
    def test_delete_operation_type_by_id(self):
        model_doc_type = self.api_wh_document_types.get_document_types()
        model_operation_type = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        self.api_wh_operation_types.delete_operation_type_by_id(model_operation_type.results[0].id)

    @allure.title('Test get list operation types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28839")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28839)
    def test_get_list_operation_types(self):
        model_doc_type = self.api_wh_document_types.get_document_types()
        model_operation_type = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        self.api_wh_operation_types.get_list_operation_types()
        self.api_wh_operation_types.delete_operation_type_by_id(model_operation_type.results[0].id)

        
    @allure.title('Test post operation types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28840")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28840)
    def test_post_operation_types(self):
        model_doc_type = self.api_wh_document_types.get_document_types()
        model_operation_type = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        self.api_wh_operation_types.delete_operation_types_by_list(model_operation_type.results[0].id)


    @allure.title('Test put update operation types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28841")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28841)
    def test_put_update_operation_types(self):
        model_doc_type = self.api_wh_document_types.get_document_types()
        model_operation_type = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        self.api_wh_operation_types.put_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None)),
            type_id=model_operation_type.results[0].id
        )
        self.api_wh_operation_types.delete_operation_types_by_list(model_operation_type.results[0].id)


    @allure.title('Test delete operation types by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28842")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28842)
    def test_delete_operation_types_by_list(self):
        model_doc_type = self.api_wh_document_types.get_document_types()
        model_operation_type1 = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        model_operation_type2 = self.api_wh_operation_types.post_operation_type(
            doc_type_id=int(next((key for key, value in model_doc_type.root.items() if value.code == "Receipt"), None))
        )
        self.api_wh_operation_types.delete_operation_types_by_list(
            model_operation_type1.results[0].id, model_operation_type2.results[0].id
        )