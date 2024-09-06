import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the companies")
class TestEsCompanies(BaseTest):

    @pytest.mark.skip(reason='Company is created in test - test_delete_company_by_id.')
    @allure.title('Test add our company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23050")
    @pytest.mark.smoke
    def test_add_our_company(self):
        self.api_es_companies.post_add_our_company()

    @allure.title('Test mark company remote by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23058")
    @pytest.mark.smoke
    def test_delete_company_by_id(self):
        created_company_id = self.api_es_companies.post_add_our_company()
        self.api_es_companies.delete_company_by_id(company_id=created_company_id)

    @allure.title('Test returns the company available to the user by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23182")
    @pytest.mark.smoke
    def test_get_company_by_id(self):
        created_company_id = self.api_es_companies.post_add_our_company()
        self.api_es_companies.get_detailed_information_on_company_by_id(company_id=created_company_id)
