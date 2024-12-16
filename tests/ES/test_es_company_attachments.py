import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsCompanyAttachments(BaseTest):

    @allure.title('Test bind the company and the attachments.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24212")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24212)
    def test_post_bind_attachments_and_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
        try:
            self.api_es_company_attachments.post_bind_attachments_and_company(
                company_id,
                attachment_id.attachmentID
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

    @allure.title('Test unbind company and attachments.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24213")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24213)
    def test_delete_unbind_attachments_and_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_es_company_attachments.post_upload_and_bind_to_company_data_from_form(company_id)
        try:
            self.api_es_company_attachments.delete_unbind_attachments_and_company(
                company_id,
                attachment_id.attachmentID
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

    @allure.title('Test uploads the file to a file server and binds it to the company, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24214")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24214)
    def test_post_upload_and_bind_to_company_data_from_form(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_es_company_attachments.post_upload_and_bind_to_company_data_from_form(company_id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

    @allure.title('Test uploads the file to a file server and binds it to the company, data from body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24215")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24215)
    def test_post_upload_bind_attachment_to_company_data_from_body(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_es_company_attachments.post_upload_bind_attachment_to_company_data_from_body(company_id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

