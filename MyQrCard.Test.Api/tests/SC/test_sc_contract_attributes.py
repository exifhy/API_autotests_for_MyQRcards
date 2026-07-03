import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service Contracts management service")
class TestContractAttributes(BaseTest):

    @allure.title('Test updates information about custom asset attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23502")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23502)
    def test_post_updates_info_about_custom_asset_attributes(self):
        company_id = self.api_es_companies.post_add_our_company()
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_contract()
        contract_id = self.api_sc_service_contract.post_method_for_add_contract(
            company_id=company_id
        )
        self.api_sc_contract_attributes.post_updates_info_about_custom_asset_attributes(
            contract_id=contract_id.contract[0],
            attribute_id=attribute_id.values[0]
        )
        self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])
        self.api_sc_service_contract.delete_contract_by_id(contract_id.contract[0])
        self.api_es_companies.delete_company_by_id(company_id)
