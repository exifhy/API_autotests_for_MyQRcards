import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonContacts(BaseTest):

    # @allure.title('Test add contacts.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23744")
    # @pytest.mark.skip(reason="Тест на создание проходит в - test_delete_contract_by_id")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(23744)
    # def test_post_add_contacts(self):
    #     self.api_common_contacts.post_add_contacts()

    @allure.title('Test delete contact by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23748")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23748)
    def test_delete_contact_by_id(self):
        contact = self.api_common_contacts.post_add_contacts()
        self.api_common_contacts.delete_contact_by_id(contact.contact[0])

    @allure.title('Test update contact by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23745")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23745)
    def test_put_update_contacts(self):
        contact_id = self.api_common_contacts.post_add_contacts()
        contact_data_first = self.api_common_contacts.get_data_contact_by_id(contact_id=contact_id.contact[0])
        self.api_common_contacts.put_update_contacts(contact_id=contact_id.contact[0])
        try:
            contact_data_second = self.api_common_contacts.get_data_contact_by_id(contact_id=contact_id.contact[0])
            assert contact_data_first.fullName != contact_data_second.fullName, \
                f'{contact_data_first.fullName} is equal {contact_data_second.fullName}'
            assert contact_data_first.description != contact_data_second.description, \
                f'{contact_data_first.description} is equal {contact_data_second.description}'
            assert contact_data_first.position != contact_data_second.position, \
                f'{contact_data_first.position} is equal {contact_data_second.position}'
        finally:
            self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])

    @allure.title('Test get list data contacts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23747")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23747)
    def test_get_list_contacts(self):
        contact = self.api_common_contacts.post_add_contacts()
        self.api_common_contacts.get_list_contacts()
        self.api_common_contacts.delete_contact_by_id(contact.contact[0])

    @allure.title('Test get data contact by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23746")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23746)
    def test_get_data_contact_by_id(self):
        contact = self.api_common_contacts.post_add_contacts()
        self.api_common_contacts.get_data_contact_by_id(contact.contact[0])
        self.api_common_contacts.delete_contact_by_id(contact.contact[0])

    @allure.title('Test delete list of contacts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23749")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23749)
    def test_delete_mass_contacts(self):
        contact_first = self.api_common_contacts.post_add_contacts()
        contact_second = self.api_common_contacts.post_add_contacts()
        contact_third = self.api_common_contacts.post_add_contacts()
        self.api_common_contacts.delete_mass_contacts(
            contact_first.contact[0],
            contact_second.contact[0],
            contact_third.contact[0]
        )
