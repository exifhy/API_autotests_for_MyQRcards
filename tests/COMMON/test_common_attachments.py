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

    @allure.title('Test upload files (many) to server V2, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25662")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25662)
    def test_post_upload_attachments_to_server_data_from_form_v2(self):
        model_attach = self.api_common_attachments.post_upload_attachments_to_server_data_from_form_v2()
        self.api_common_attachments.delete_attachments_by_list(
            model_attach.results[0].attachmentID, model_attach.results[1].attachmentID
        )

    @allure.title('Test delete attachments by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25675")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25675)
    @pytest.mark.skip(reason="Тест на массовое удаление вложения проходит "
                             "в - test_post_upload_attachments_to_server_data_from_form_v2")
    def test_delete_attachments_by_list(self):
        model_attach = self.api_common_attachments.post_upload_attachments_to_server_data_from_form_v2()
        self.api_common_attachments.delete_attachments_by_list(
            model_attach.results[0].attachmentID, model_attach.results[1].attachmentID
        )

    @allure.title('Test upload file to server, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25663")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25663)
    def test_post_upload_attachment_data_from_body(self):
        model_attach = self.api_common_attachments.post_upload_attachment_data_from_body()
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test get download attachment (noRedirect=true).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25664")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25664)
    def test_get_download_attachment_no_redirect_true(self):
        model_attach = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        self.api_common_attachments.get_download_attachment_no_redirect_true(model_attach.attachmentID)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test get TemporaryRedirect to a temporary link for downloading the attachment.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25665")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25665)
    def test_get_downloading_attachment(self):
        model_attach = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        self.api_common_attachments.get_downloading_attachment(model_attach)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test get list attachments for current user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25666")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25666)
    def test_get_list_attachments_for_current_user(self):
        self.api_common_attachments.get_list_attachments_for_current_user()

    @allure.title('Test get list attachments for current user by attachmentID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25668")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25668)
    def test_get_list_attachments_for_current_user_by_attachment_id(self):
        model_attach = self.api_common_attachments.post_upload_attachment_data_from_body()
        self.api_common_attachments.get_list_attachments_for_current_user_by_attachment_id(model_attach.attachmentID)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test get list attachments for current user. isDeleted=true.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25669")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25669)
    def test_get_list_attachments_for_current_user_is_deleted_true(self):
        self.api_common_attachments.get_list_attachments_for_current_user_deleted(True)

    @allure.title('Test get list attachments for current user. isDeleted=false.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25670")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25670)
    def test_get_list_attachments_for_current_user_is_deleted_false(self):
        self.api_common_attachments.get_list_attachments_for_current_user_deleted(False)

    @allure.title('Test get attachment data by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25667")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25667)
    def test_get_attachment_data_by_id(self):
        model_attach = self.api_common_attachments.post_upload_attachment_data_from_body()
        self.api_common_attachments.get_attachment_data_by_id(model_attach)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test publish attachment by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25672")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25672)
    @pytest.mark.skip(reason="Тест на публикацию проходит в - test_post_unpublish_attachment_by_id.")
    def test_post_publish_attachment_by_id(self):
        model_attach = self.api_common_attachments.post_upload_attachment_data_from_body()
        self.api_common_attachments.post_publish_attachment_by_id(model_attach.attachmentID)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test unpublish attachment by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25673")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25673)
    def test_post_unpublish_attachment_by_id(self):
        model_attach = self.api_common_attachments.post_upload_attachment_data_from_body()
        self.api_common_attachments.post_publish_attachment_by_id(model_attach.attachmentID)
        self.api_common_attachments.post_unpublish_attachment_by_id(model_attach.attachmentID)
        self.api_common_attachments.delete_attachment_by_id(model_attach.attachmentID)

    @allure.title('Test get attachment download link for task.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25674")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25674)
    def test_get_attachment_download_link_for_task(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
        attachment_id = self.api_work_task_attachments.post_upload_bind_attachment_to_task_data_from_body(
            model_task.id
        )
        self.api_common_attachments.get_attachment_download_link_for_task(model_task.id)
        self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)
        self.api_work_tasks.delete_task_by_id(model_task.id)
