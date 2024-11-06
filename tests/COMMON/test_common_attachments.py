import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonAttachments(BaseTest):

    @allure.title('Test upload file to server, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23805")
    @pytest.mark.skip(reason="Тест на загрузку вложения проходит в - test_delete_attachment_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23805)
    def test_post_upload_attachments_to_server_data_from_form(self):
        self.api_common_attachments.post_upload_attachments_to_server_data_from_form()

    @allure.title('Test delete attachment by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23807")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23807)
    def test_delete_attachment_by_id(self):
        attachment_id = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)
