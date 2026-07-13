import allure
import pytest
from allure_commons.types import Severity
from loguru import logger
from requests import JSONDecodeError

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


@pytest.mark.test_scripts_suites_es_company_attachments
class TestEsCompanyAttachmentsScriptSuite(BaseTest):

    @allure.title('Test script ES/companyAttachments (POST, GET, PUT, GET, DELETE by list, GET).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_company_attachments_add_from_form_get_delete_by_list_get(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i + 1}]")):
                try:
                    attachment_id = self.api_es_company_attachments.post_upload_and_bind_to_company_data_from_form(
                        company_id
                    )
                    model_attachments = self.api_es_companies.get_list_attachments_from_company(
                        company_id,
                        False
                    )
                    assert str(attachment_id.attachmentID) in model_attachments.root, \
                        f'Attachment with ID {attachment_id.attachmentID} is not in list attachments company'
                    self.api_es_company_attachments.delete_unbind_attachments_and_company(
                        company_id,
                        attachment_id.attachmentID
                    )
                    self.api_es_companies.get_list_attachments_from_company(
                        company_id,
                        True
                    )
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i + 1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
