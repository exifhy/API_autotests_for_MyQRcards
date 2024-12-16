import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsCompanies(BaseTest):

    @pytest.mark.skip(reason='Company is created in test - test_delete_company_by_id.')
    @allure.title('Test add our company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23050")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23050)
    def test_add_our_company(self):
        self.api_es_companies.post_add_our_company()

    @allure.title('Test delete company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23058")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23058)
    def test_delete_company_by_id(self):
        created_company_id = self.api_es_companies.post_add_our_company()
        self.api_es_companies.delete_company_by_id(company_id=created_company_id)

    @allure.title('Test delete company by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23056")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23056)
    def test_delete_company_by_list(self):
        company_id_first = self.api_es_companies.post_add_our_company()
        company_id_second = self.api_es_companies.post_add_our_company()
        self.api_es_companies.delete_companies_by_list(company_id_first, company_id_second)

    @allure.title('Test returns the company available to the user by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23182")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23182)
    def test_get_company_by_id(self):
        created_company_id = self.api_es_companies.post_add_our_company()
        self.api_es_companies.get_detailed_information_on_company_by_id(company_id=created_company_id)

    @allure.title('Test returns a list of companies available to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23287")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23287)
    def test_get_list_companies(self):
        self.api_es_companies.get_list_companies()

    @allure.title('Test update company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23288")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23288)
    def test_put_update_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        model_company = self.api_es_companies.get_detailed_information_on_company_by_id(company_id)
        self.api_es_companies.put_update_company_by_id(
            company_id=company_id,
            customer_id=model_company.customerOrgUnit.id,
            staff_id=model_company.staffOrgUnit.id
        )
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test returns a head companies.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24256")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24256)
    def test_head_companies(self):
        self.api_es_companies.head_companies()

    @allure.title('Test get a list company attachments.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24228")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24228)
    def test_get_list_attachments_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_es_company_attachments.post_upload_and_bind_to_company_data_from_form(company_id)
        try:
            self.api_es_companies.get_list_attachments_from_company(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

    @allure.title('Test download attachment from company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24229")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24229)
    def test_get_download_attachment_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_es_company_attachments.post_upload_and_bind_to_company_data_from_form(company_id)
        try:
            self.api_es_companies.get_download_attachment_from_company(company_id, attachment_id.attachmentID)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

    @allure.title('Test get info attachment file from company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24230")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24230)
    def test_get_attachment_info_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        attachment_id = self.api_es_company_attachments.post_upload_and_bind_to_company_data_from_form(company_id)
        try:
            self.api_es_companies.get_attachment_info_from_company(company_id, attachment_id.attachmentID)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id.attachmentID)

    @allure.title('Test add attributes to company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24232")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24232)
    def test_post_update_company_attributes(self):
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_company_str()
        try:
            self.api_es_companies.post_update_company_attributes(company_id, attribute_id.values[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_attributes.delete_method_attribute_by_id(attribute_id.values[0])

    @allure.title('Test get company attributes by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24231")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24231)
    def test_get_attributes_info_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        try:
            self.api_es_companies.get_attributes_info_from_company(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test add bank account to company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24246")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24246)
    def test_post_add_bank_accounts_to_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        bank_id = self.api_common_banks.get_list_banks_return_first_id()
        try:
            self.api_es_companies.post_add_bank_accounts_to_company(
                company_id,
                bank_id
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test get company bank accounts by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24233")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24233)
    def test_get_bank_accounts_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        bank_id = self.api_common_banks.get_list_banks_return_first_id()
        try:
            self.api_es_companies.post_add_bank_accounts_to_company(
                company_id,
                bank_id
            )
            self.api_es_companies.get_bank_accounts_from_company(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test update company bank accounts by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24245")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24245)
    def test_put_update_company_bank_accounts(self):
        company_id = self.api_es_companies.post_add_our_company()
        bank_id = self.api_common_banks.get_list_banks_return_first_id()
        try:
            model_bank = self.api_es_companies.post_add_bank_accounts_to_company(
                company_id,
                bank_id
            )
            bank_before = self.api_es_companies.get_bank_accounts_from_company(company_id)
            self.api_es_companies.put_update_company_bank_accounts(
                company_id,
                bank_id,
                model_bank.result[0].companyBankAccountID
            )
            bank_after = self.api_es_companies.get_bank_accounts_from_company(company_id)
            assert bank_after != bank_before, f'{bank_after} is equal {bank_before}'
        finally:
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test delete bank accounts from company by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24248")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24248)
    def test_delete_bank_accounts_from_company_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        bank_id = self.api_common_banks.get_list_banks_return_first_id()
        try:
            model_bank = self.api_es_companies.post_add_bank_accounts_to_company(
                company_id,
                bank_id
            )
            self.api_es_companies.delete_bank_accounts_from_company_by_list(
                company_id,
                model_bank.result[0].companyBankAccountID
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test delete bank accounts from company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24249")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24249)
    def test_delete_bank_accounts_from_company_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        bank_id = self.api_common_banks.get_list_banks_return_first_id()
        try:
            model_bank = self.api_es_companies.post_add_bank_accounts_to_company(
                company_id,
                bank_id
            )
            self.api_es_companies.delete_bank_account_from_company_by_id(
                company_id,
                model_bank.result[0].companyBankAccountID
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test get list contacts from company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24250")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24250)
    def test_get_list_contacts_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_companies.post_add_contact_to_company_by_id(company_id, contact_id.contact[0])
            self.api_es_companies.get_list_contacts_from_company(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])

    @allure.title('Test get list contacts from company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24251")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24251)
    def test_get_contact_from_company_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_companies.post_add_contact_to_company_by_id(company_id, contact_id.contact[0])
            self.api_es_companies.get_contact_from_company_by_id(company_id, contact_id.contact[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])

    @allure.title('Test add contact to company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24252")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24252)
    def test_post_add_contact_to_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_companies.post_add_contact_to_company_by_id(company_id, contact_id.contact[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])

    @allure.title('Test delete contact from company by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24253")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24253)
    def test_delete_contact_from_company_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        contact_id = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_companies.post_add_contact_to_company_by_id(company_id, contact_id.contact[0])
            self.api_es_companies.delete_contact_from_company_by_id(company_id, contact_id.contact[0])
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])

    @allure.title('Test add contacts to company by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24254")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24254)
    def test_post_add_contacts_to_company_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        contact_id_first = self.api_common_contacts.post_add_contacts()
        contact_id_second = self.api_common_contacts.post_add_contacts()
        contact_id_third = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_companies.post_add_contacts_to_company_by_list(
                company_id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_contacts.delete_mass_contacts(
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )

    @allure.title('Test delete contacts from company by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24255")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24255)
    def test_delete_contacts_from_company_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        contact_id_first = self.api_common_contacts.post_add_contacts()
        contact_id_second = self.api_common_contacts.post_add_contacts()
        contact_id_third = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_companies.post_add_contacts_to_company_by_list(
                company_id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
            self.api_es_companies.delete_contacts_from_company_by_list(
                company_id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_common_contacts.delete_mass_contacts(
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )

    @allure.title('Test get find dadata company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24258")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24258)
    def test_find_dadata_company(self):
        self.api_es_companies.get_find_dadata_company(inn=7707661329)

    @allure.title('Test get actual location from company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24259")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24259)
    def test_get_actual_location_from_company(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        try:
            self.api_es_company_locations.post_add_company_locations(company_id, location_id)
            self.api_es_companies.get_actual_company_location(company_id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
