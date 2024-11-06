import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service Contracts management service")
class TestScServiceContract(BaseTest):

    @allure.story('Story: Contract')
    class TestContract(BaseTest):

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

    @allure.story('Story: Contract and attributes')
    class TestContractAttributes(BaseTest):

        @allure.title('Test method of get list user attributes by contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23689")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23689)
        def test_get_list_user_attributes_contract(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            self.api_sc_service_contract.get_list_user_attributes_contract(contract_id=contract_id.contract[0])
            self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
            self.api_es_companies.delete_company_by_id(company_id)

    @allure.story('Story: Contracts and assets')
    class TestContractAssets(BaseTest):

        @allure.title('Test add a list of objects to the contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23572")
        @pytest.mark.skip(reason="Тест проходит в - test_delete_objects_related_to_contracts_by_id")
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

        @allure.title('Test method of mass deleting objects related with a service contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23690")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23690)
        def test_delete_objects_related_to_contracts(self):
            company_id = self.api_es_companies.post_add_our_company()
            location_id = self.api_es_locations.post_add_location()
            self.api_es_company_locations.post_add_company_locations(
                company_id=company_id,
                location_id=location_id
            )
            asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
            asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
            asset_id_first = self.api_es_assets.post_add_object(
                company_id=company_id,
                asset_class_id=asset_class_id,
                asset_type_id=asset_type_id
            )
            asset_id_second = self.api_es_assets.post_add_object(
                company_id=company_id,
                asset_class_id=asset_class_id,
                asset_type_id=asset_type_id
            )
            asset_id_third = self.api_es_assets.post_add_object(
                company_id=company_id,
                asset_class_id=asset_class_id,
                asset_type_id=asset_type_id
            )
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id=company_id)
            try:
                self.api_sc_service_contract.post_add_list_with_three_objects_to_contract(
                    contract_id=contract_id.contract[0],
                    asset_id_first=asset_id_first.id,
                    asset_id_second=asset_id_second.id,
                    asset_id_third=asset_id_third.id
                )
                asset_ids = asset_id_first.id, asset_id_second.id, asset_id_third.id
                self.api_sc_service_contract.delete_objects_related_to_contracts(
                    contract_id.contract[0],
                    *asset_ids
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id.contract[0])
                self.api_es_assets.delete_object_by_id(asset_id=asset_id_first.id)
                self.api_es_assets.delete_object_by_id(asset_id=asset_id_second.id)
                self.api_es_assets.delete_object_by_id(asset_id=asset_id_third.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

        @allure.title('Test method of deleting objects related with a service contract by ID.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23691")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23691)
        def test_delete_objects_related_to_contracts_by_id(self):
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
                self.api_sc_service_contract.delete_objects_related_to_contracts_by_id(
                    contract_id.contract[0],
                    asset_id=asset_id.id
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id.contract[0])
                self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

        @allure.title('Test method of get the list of service contract objects.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23692")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23692)
        def test_get_list_of_contract_objects(self):
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
                self.api_sc_service_contract.get_list_of_contract_objects(contract_id.contract[0])
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id.contract[0])
                self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

        @allure.title('Test add object to contract by ID.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23696")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23696)
        def test_put_add_object_to_contracts_by_id(self):
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
                self.api_sc_service_contract.put_add_object_to_contracts_by_id(
                    contract_id=contract_id.contract[0],
                    asset_id=asset_id.id
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id.contract[0])
                self.api_es_assets.delete_object_by_id(asset_id=asset_id.id)
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_location_by_id(location_id)

    @allure.story('Story: Contracts and attachments')
    class TestContractAttachments(BaseTest):

        @allure.title('Test upload file to server and bind to contract, data from form.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23720")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23720)
        def test_post_upload_file_to_server_and_bind_contract_data_from_form(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            try:
                self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_form(
                    contract_id=contract_id.contract[0]
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test method to get TemporaryRedirect to a temporary link to download a file.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23753")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23753)
        def test_get_temporary_redirect_to_temporary_download_link(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            attachment_id = self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_form(
                contract_id=contract_id.contract[0]
            )
            self.api_sc_service_contract.get_temporary_redirect_to_temporary_download_link(
                contract_id=contract_id.contract[0],
                attachment_id=attachment_id.attachmentID
            )
            self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
            self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test upload file to server and bind to contract, data from body.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23730")
        @pytest.mark.xfail(reason="Ручка срабатывает через раз. Возможен баг.")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23730)
        def test_post_upload_file_to_server_and_bind_contract_data_from_body(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            try:
                self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_body(
                    contract_id.contract[0]
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test method of get the list of attachments bind to contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23725")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23725)
        def test_get_list_of_attachments_contract(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_form(
                contract_id.contract[0]
            )
            self.api_sc_service_contract.get_list_of_attachments_contract(contract_id.contract[0])
            self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
            self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test method of mass attachment bind to a contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23726")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23726)
        def test_post_bind_contract_and_attachment_by_list_id(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            contract_id_second = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            attachment_id = self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_form(
                contract_id.contract[0]
            )
            try:
                self.api_sc_service_contract.post_bind_contract_and_attachment_by_list_id(
                    contract_id_second.contract[0],
                    attachment_id.attachmentID
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id_second.contract[0])
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test method of get of attachment binds to contract by id.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23752")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23752)
        def test_get_attachment_bind_contract_by_id(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            attachment_id = self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_form(
                contract_id.contract[0]
            )
            try:
                self.api_sc_service_contract.get_attachment_bind_contract_by_id(
                    contract_id=contract_id.contract[0],
                    attachment_id=attachment_id.attachmentID
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test delete attachment from contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23754")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23754)
        def test_delete_attachment_from_contract(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            attachment_id = self.api_sc_service_contract.post_upload_file_to_server_and_bind_contract_data_from_form(
                contract_id.contract[0]
            )
            try:
                self.api_sc_service_contract.delete_attachment_from_contract(
                    contract_id.contract[0],
                    attachment_id.attachmentID
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_es_companies.delete_company_by_id(company_id)

    @allure.story('Story: Contracts and contacts')
    class TestContractContacts(BaseTest):

        @allure.title('Test method of adding contacts to contracts.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23757")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23757)
        def test_post_add_contacts_to_contract(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            contact_id = self.api_common_contacts.post_add_contacts()
            contact_id_second = self.api_common_contacts.post_add_contacts()
            try:
                self.api_sc_service_contract.post_add_contacts_to_contract(
                    contract_id.contract[0],
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_common_contacts.delete_mass_contacts(
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test method get the list of contacts of those responsible for the contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23755")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23755)
        def test_get_list_of_contacts_by_contract(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            contact_id = self.api_common_contacts.post_add_contacts()
            contact_id_second = self.api_common_contacts.post_add_contacts()
            try:
                self.api_sc_service_contract.post_add_contacts_to_contract(
                    contract_id.contract[0],
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
                self.api_sc_service_contract.get_list_of_contacts_by_contract(
                    contract_id=contract_id.contract[0]
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_common_contacts.delete_mass_contacts(
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test delete contacts from contract.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23756")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23756)
        def test_delete_contracts_from_contract(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            contact_id = self.api_common_contacts.post_add_contacts()
            contact_id_second = self.api_common_contacts.post_add_contacts()
            try:
                self.api_sc_service_contract.post_add_contacts_to_contract(
                    contract_id.contract[0],
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
                self.api_sc_service_contract.delete_contracts_from_contract(
                    contract_id.contract[0],
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_common_contacts.delete_mass_contacts(
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test delete contacts from contract by ID.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23758")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23758)
        def test_delete_contract_from_contract_by_id(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            contact_id = self.api_common_contacts.post_add_contacts()
            try:
                self.api_sc_service_contract.post_add_contacts_to_contract(
                    contract_id.contract[0],
                    contact_id.contact[0],
                )
                self.api_sc_service_contract.delete_contract_from_contract_by_id(
                    contract_id.contract[0],
                    contact_id.contact[0],
                )
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_common_contacts.delete_mass_contacts(
                    contact_id.contact[0],
                )
                self.api_es_companies.delete_company_by_id(company_id)

        @allure.title('Test method of adding contact to contract by ID.')
        @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23759")
        @pytest.mark.regress
        @pytest.mark.test_case_id(23759)
        def test_put_add_contact_to_contract_by_id(self):
            company_id = self.api_es_companies.post_add_our_company()
            contract_id = self.api_sc_service_contract.post_method_for_add_contract(company_id)
            contact_id = self.api_common_contacts.post_add_contacts()
            contact_id_second = self.api_common_contacts.post_add_contacts()
            try:
                self.api_sc_service_contract.post_add_contacts_to_contract(
                    contract_id.contract[0],
                    contact_id.contact[0]
                )
                self.api_sc_service_contract.put_add_contact_to_contract_by_id(
                    contract_id.contract[0],
                    contact_id_second.contact[0]
                )
                model_contacts = self.api_sc_service_contract.get_list_of_contacts_by_contract(
                    contract_id=contract_id.contract[0]
                )
                assert model_contacts.root[str(contact_id.contact[0])].contractID == contract_id.contract[0], \
                    f'The contact with ID {contact_id.contact[0]} did not add to the contract ID{contract_id.contract[0]}'
                assert model_contacts.root[str(contact_id_second.contact[0])].contractID == contract_id.contract[0], \
                    f'The contact with ID {contact_id_second.contact[0]} did not add to the contract ID{contract_id.contract[0]}'
            finally:
                self.api_sc_service_contract.delete_contract_by_id(contract_id=contract_id.contract[0])
                self.api_common_contacts.delete_mass_contacts(
                    contact_id.contact[0],
                    contact_id_second.contact[0]
                )
                self.api_es_companies.delete_company_by_id(company_id)
