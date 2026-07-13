import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service offers application programming interface for warehouses.")
class TestWhDocumentTypes(BaseTest):

    @allure.title('Test get document types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/28844")
    @pytest.mark.regress
    @pytest.mark.test_case_id(28844)
    def test_get_document_types(self):
        self.api_wh_document_types.get_document_types()
