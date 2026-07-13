import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestOrgUnits(BaseTest):

    @allure.title('Test get root org units.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24303")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24303)
    def test_get_root_org_units(self):
        self.api_es_org_units.get_root_org_units()

    @allure.title('Test get root org units by company ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24313")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24303)
    def test_get_root_org_units_by_company_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_org_units.get_root_org_units_by_company_id(company_id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test get org units by company ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24314")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24314)
    def test_get_org_units_by_company_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        self.api_es_org_units.get_org_units_by_company_id(company_id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test get org units.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24305")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24305)
    def test_get_org_units(self):
        self.api_es_org_units.get_org_units()

    @allure.title('Test get org units by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24306")
    @pytest.mark.skip(reason="Неизвестен ID")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24306)
    def test_get_org_units_by_id(self):
        self.api_es_org_units.get_org_units_by_id(1)
