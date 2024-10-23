import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service Contracts management service")
class TestScServiceContract(BaseTest):

    @allure.title('Test method of get the total number of service contracts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23582")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23582)
    def test_head_method_total_count_of_contract(self):
        self.api_sc_service_contract.head_method_total_count_of_contract()

    @allure.title('Test method for creating or updating service contract(s).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23508")
    @pytest.mark.skip(reason="Тест на создание проходит в - test_delete_contract_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23508)
    def test_post_method_for_add_contract(self):
        company_id = self.api_es_companies.post_add_our_company()
        self.api_sc_service_contract.post_method_for_add_contract(company_id)

    @allure.title('Test method for deleting a contract by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23577")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23577)
    def test_delete_contract_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
        self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test method for mass deletion of contracts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23578")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23578)
    def test_delete_mass_of_contracts(self):
        company_id = self.api_es_companies.post_add_our_company()
        contract_id_first = self.api_sc_service_contract.post_method_for_add_contract(company_id)
        contract_id_second = self.api_sc_service_contract.post_method_for_add_contract(company_id)
        contract_id_third = self.api_sc_service_contract.post_method_for_add_contract(company_id)
        params = contract_id_first.contract[0], contract_id_second.contract[0], contract_id_third.contract[0]
        self.api_sc_service_contract.delete_mass_of_contract(*params)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test method of get list service contract.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23581")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23581)
    def test_get_list_service_contracts(self):
        self.api_sc_service_contract.get_list_service_contracts()

    @allure.title('Test method of get service contract by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23580")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23580)
    def test_get_contract_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        contract = self.api_sc_service_contract.post_add_contract_return_data_contract(company_id)
        try:
            model_contract = self.api_sc_service_contract.get_contract_by_id(contract_id=contract[0])
            assert company_id == model_contract.companyID, \
                f'Expected company ID <{company_id}>, but got <{model_contract.companyID}>'

            assert contract[0] == model_contract.contractID, \
                f'Expected contract ID <{contract[0]}>, but got <{model_contract.contractID}>'

            assert contract[1] == model_contract.name, \
                f'Expected contract name <{contract[1]}>, but got <{model_contract.name}>'

            assert contract[2] == model_contract.description, \
                f'Expected description contract <{contract[2]}>, but got <{model_contract.description}>'

            assert contract[3] == model_contract.conditions, \
                f'Expected conditions contract <{contract[3]}>, but got <{model_contract.conditions}>'
        finally:
            self.api_sc_service_contract.delete_contract_by_id(contract_id=contract[0])
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test method for updating service contract(s).')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23684")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23684)
    def test_put_update_method_for_exist_contract(self):
        company_id_first = self.api_es_companies.post_add_our_company()
        company_id_second = self.api_es_companies.post_add_our_company()
        contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id_first)
        model_first = self.api_sc_service_contract.get_contract_by_id(contract_id=contract_id.contract[0])
        self.api_sc_service_contract.put_update_method_for_exist_contract(
            contract_id=contract_id.contract[0],
            company_id=company_id_second
        )
        model_second = self.api_sc_service_contract.get_contract_by_id(contract_id=contract_id.contract[0])
        try:
            assert model_first.name != model_second.name, \
                f'<{model_first.name}> is equal <{model_second.name}>.'

            assert model_first.companyID != model_second.companyID, \
                f'<{model_first.companyID}> is equal <{model_second.companyID}>.'

            assert model_first.description != model_second.description, \
                f'<{model_first.description}> is equal <{model_second.description}>.'

            assert model_first.conditions != model_second.conditions, \
                f'<{model_first.conditions}> is equal <{model_second.conditions}>.'

            assert model_first.dateFrom != model_second.dateFrom, \
                f'<{model_first.dateFrom}> is equal <{model_second.dateFrom}>.'

        finally:
            self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
            self.api_es_companies.delete_company_by_id(company_id_first)
            self.api_es_companies.delete_company_by_id(company_id_second)

    @allure.title('Test add a list of objects to the contract.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23572")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23572)
    def test_post_add_list_object_to_contract(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        asset_id = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id=company_id)
        try:
            self.api_sc_service_contract.post_add_list_object_to_contract(
                contract_id=contract_id.contract[0],
                asset_id=asset_id.id
            )
        finally:
            self.api_sc_service_contract.delete_contract_by_id(contract_id.contract[0])
            self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
