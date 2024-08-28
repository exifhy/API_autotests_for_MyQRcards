import allure
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the companies")
class TestEsCompanies(BaseTest):

    @allure.title('Test add our company.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23050")
    def test_add_our_company(self):
        self.api_es_companies.post_add_our_company()

    @allure.title('Test mark company remote by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23058")
    def test_delete_company_by_id(self):
        created_company_id = self.api_es_companies.post_add_our_company()
        self.api_es_companies.delete_company_by_id(company_id=created_company_id)
