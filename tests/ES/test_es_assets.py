from json import JSONDecodeError
import allure
import pytest
from allure_commons.types import Severity
from config.base_test import BaseTest
from src.enums.params_enums import Params
from loguru import logger


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssets(BaseTest):

    @allure.title('Test returns the directory of objects available to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23025")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23025)
    @pytest.mark.parametrize('param', Params.params_assets_list.value)
    def test_get_directory_of_objects_available_to_user(self, param):
        self.api_es_assets.get_asset_available_to_user(param, None)

    @pytest.mark.smoke
    @pytest.mark.skip(reason='Asset is created in test - test_delete_object_by_id.')
    @pytest.mark.test_case_id(23026)
    @allure.title('Test object creation.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23026")
    def test_post_add_object(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

    @allure.title('Test marks the object as deleted.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23027")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23027)
    def test_delete_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test detailed information on the object by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23031")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23031)
    def test_get_detailed_information_on_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_assets.get_detailed_information_on_object_by_id(object_model.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test object publication.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23078")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23078)
    def test_put_method_of_publishing_an_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=created_location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(created_location_id)

    @allure.title('Test object publication without location.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23084")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23084)
    def test_put_method_of_publishing_an_object_by_id_without_location(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id_without_location(object_model.id)
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test update the object by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23080")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23080)
    def test_put_update_object_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_new_object = self.api_es_assets.get_detailed_information_on_object_by_id(object_model.id)
        self.api_es_assets.put_update_object_by_id(
            asset_id=object_model.id,
            company_id=company_id,
            asset_type_id=asset_type_id,
            asset_class_id=asset_class_id
        )
        model_update_object = self.api_es_assets.get_detailed_information_on_object_by_id(object_model.id)
        assert model_new_object.name != model_update_object.name, (f'Object update error,'
                                                                   f'{model_update_object.name} = '
                                                                   f'{model_new_object.name}')
        assert model_new_object.notes != model_update_object.notes, (f'Object update error,'
                                                                     f'{model_update_object.notes} = '
                                                                     f'{model_new_object.notes}')
        self.api_es_assets.delete_object_by_id(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get the list of assignments of the specified asset to users.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23894")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23894)
    def test_get_list_assignment_of_asset_to_user(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assets.get_list_assignment_of_asset_to_user(object_model.id)
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get the list asset attachments.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23923")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23923)
    def test_get_list_asset_attachments(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

        attachment_id = self.api_es_asset_attachments.post_upload_file_to_server_and_bind_asset(
            asset_id=model_asset.id
        )
        try:
            self.api_es_assets.get_list_asset_attachments(asset_id=model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)

    @allure.title('Test get the list asset attachment by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23924")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23924)
    def test_get_list_asset_attachment_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

        attachment_id = self.api_es_asset_attachments.post_upload_file_to_server_and_bind_asset(
            asset_id=model_asset.id
        )
        try:
            self.api_es_assets.get_list_asset_attachment_by_id(
                asset_id=model_asset.id,
                attach_id=attachment_id.attachmentID
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attachments.delete_attachment_by_id(attachment_id=attachment_id.attachmentID)

    @allure.title('Test get the list asset attributes.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23926")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23926)
    def test_get_list_asset_attributes(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        attribute_id = self.api_common_attributes.post_add_method_attributes_only_for_asset_str()
        try:
            self.api_es_asset_attributes.post_update_attributes_assets(
                asset_id=model_asset.id,
                attribute_id=attribute_id.values[0]
            )
            self.api_es_assets.get_list_asset_attributes(asset_id=model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_attributes.delete_method_attribute_by_id(attribute_id=attribute_id.values[0])

    @allure.title(
        'Test upload a JPG image of at least 128x128 to be used as an avatar for asset, data from the form.'
    )
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23928")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23928)
    def test_put_upload_avatar_for_asset_data_from_form(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assets.put_upload_avatar_for_asset_data_from_form(model_asset.id)
        finally:
            self.api_es_assets.delete_avatar_from_asset_by_id(asset_id=model_asset.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test upload a JPG image of at least 128x128 to be used as an avatar for asset, data from the body.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23929")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23929)
    def test_put_upload_avatar_for_asset_data_from_body(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assets.put_upload_avatar_for_asset_data_from_body(model_asset.id)
        finally:
            self.api_es_assets.delete_avatar_from_asset_by_list(model_asset.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete avatar from asset by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23930")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23930)
    def test_delete_avatar_from_asset_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assets.put_upload_avatar_for_asset_data_from_body(model_asset.id)
            self.api_es_assets.delete_avatar_from_asset_by_id(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete avatar from asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23931")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23931)
    def test_delete_avatar_from_asset_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assets.put_upload_avatar_for_asset_data_from_form(model_asset.id)
            self.api_es_assets.delete_avatar_from_asset_by_list(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test add checklists to asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23933")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23933)
    def test_post_add_checklists_to_asset_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_checklist = self.api_work_checklists.post_add_checklists()
        try:
            self.api_es_assets.post_add_checklists_to_asset_by_list(model_asset.id, model_checklist.result[0])
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test get the list asset checklists.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23932")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23932)
    def test_get_list_asset_checklists(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        checklist_id = self.api_work_checklists.post_add_checklists()
        model_checklist = self.api_work_checklists.get_checklist_by_id(checklist_id.result[0])
        try:
            self.api_es_assets.post_add_checklists_to_asset_by_list(model_asset.id, checklist_id.result[0])
            model_asset_checklist = self.api_es_assets.get_list_asset_checklists(model_asset.id)
            for id_, checklist in model_asset_checklist.root.items():
                assert checklist[0].name == model_checklist.name, \
                    f'Expected {checklist[0].name}, but got {model_checklist.name}.'
                assert checklist[0].description == model_checklist.description, \
                    f'Expected {checklist[0].description}, but got {model_checklist.description}.'
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_work_checklists.delete_checklist_by_id(checklist_id.result[0])

    @allure.title('Test add checklists to asset by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23935")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23935)
    def test_post_add_checklist_to_asset_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_checklist = self.api_work_checklists.post_add_checklists()
        try:
            self.api_es_assets.post_add_checklist_to_asset_by_id(model_asset.id, model_checklist.result[0])
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test delete checklists from asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23934")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23934)
    def test_delete_checklists_from_asset_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_checklist_first = self.api_work_checklists.post_add_checklists()
        model_checklist_second = self.api_work_checklists.post_add_checklists()
        model_checklist_third = self.api_work_checklists.post_add_checklists()
        try:
            self.api_es_assets.post_add_checklists_to_asset_by_list(
                model_asset.id,
                model_checklist_first.result[0],
                model_checklist_second.result[0],
                model_checklist_third.result[0]
            )
            self.api_es_assets.delete_checklists_from_asset_by_list(
                model_asset.id,
                model_checklist_first.result[0],
                model_checklist_second.result[0],
                model_checklist_third.result[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_work_checklists.delete_checklist_by_list(
                model_checklist_first.result[0],
                model_checklist_second.result[0],
                model_checklist_third.result[0]
            )

    @allure.title('Test delete checklists from asset by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23936")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23936)
    def test_delete_checklists_from_asset_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_checklist_first = self.api_work_checklists.post_add_checklists()
        try:
            self.api_es_assets.post_add_checklist_to_asset_by_id(
                model_asset.id,
                model_checklist_first.result[0]
            )
            self.api_es_assets.delete_checklist_from_asset_by_id(
                model_asset.id,
                model_checklist_first.result[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist_first.result[0])

    @allure.title('Test add a contact person for the asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23958")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23958)
    def test_post_add_contact_person_for_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contact_id = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_assets.post_add_contact_person_for_asset(
                model_asset.id,
                contact_id.contact[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_contact_by_id(contact_id.contact[0])

    @allure.title('Test add a contact persons for the asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23959")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23959)
    def test_post_add_contact_persons_for_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contact_id_first = self.api_common_contacts.post_add_contacts()
        contact_id_second = self.api_common_contacts.post_add_contacts()
        contact_id_third = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_assets.post_add_contact_persons_for_asset(
                model_asset.id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_mass_contacts(
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )

    @allure.title('Test get a list of valid contacts for the asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23960")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23960)
    def test_get_list_valid_contacts_for_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contact_id_first = self.api_common_contacts.post_add_contacts()
        contact_id_second = self.api_common_contacts.post_add_contacts()
        contact_id_third = self.api_common_contacts.post_add_contacts()
        try:
            model_contact_first = self.api_common_contacts.get_data_contact_by_id(contact_id_first.contact[0])
            model_contact_second = self.api_common_contacts.get_data_contact_by_id(contact_id_second.contact[0])
            model_contact_third = self.api_common_contacts.get_data_contact_by_id(contact_id_third.contact[0])
            self.api_es_assets.post_add_contact_persons_for_asset(
                model_asset.id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
            model_asset_contacts = self.api_es_assets.get_list_valid_contacts_for_asset(model_asset.id)
            for id_contact, value_contact in model_asset_contacts.root.items():
                match int(id_contact):
                    case model_contact_first.id:
                        assert value_contact.fullName == model_contact_first.fullName, \
                            f'Expected {value_contact.fullName}, but got {model_contact_first.fullName}.'
                        assert value_contact.description == model_contact_first.description, \
                            f'Expected {value_contact.description}, but got {model_contact_first.description}.'
                        assert value_contact.position == model_contact_first.position, \
                            f'Expected {value_contact.position}, but got {model_contact_first.position}.'
                        assert value_contact.email == model_contact_first.email, \
                            f'Expected {value_contact.email}, but got {model_contact_first.email}.'
                    case model_contact_second.id:
                        assert value_contact.fullName == model_contact_second.fullName, \
                            f'Expected {value_contact.fullName}, but got {model_contact_second.fullName}.'
                        assert value_contact.description == model_contact_second.description, \
                            f'Expected {value_contact.description}, but got {model_contact_second.description}.'
                        assert value_contact.position == model_contact_second.position, \
                            f'Expected {value_contact.position}, but got {model_contact_second.position}.'
                        assert value_contact.email == model_contact_second.email, \
                            f'Expected {value_contact.email}, but got {model_contact_second.email}.'
                    case model_contact_third.id:
                        assert value_contact.fullName == model_contact_third.fullName, \
                            f'Expected {value_contact.fullName}, but got {model_contact_third.fullName}.'
                        assert value_contact.description == model_contact_third.description, \
                            f'Expected {value_contact.description}, but got {model_contact_third.description}.'
                        assert value_contact.position == model_contact_third.position, \
                            f'Expected {value_contact.position}, but got {model_contact_third.position}.'
                        assert value_contact.email == model_contact_third.email, \
                            f'Expected {value_contact.email}, but got {model_contact_third.email}.'

        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_mass_contacts(
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )

    @allure.title('Test get valid contact for the asset by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23961")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23961)
    def test_get_valid_contact_for_asset_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contact_id_first = self.api_common_contacts.post_add_contacts()
        try:
            model_contact_first = self.api_common_contacts.get_data_contact_by_id(contact_id_first.contact[0])
            self.api_es_assets.post_add_contact_persons_for_asset(
                model_asset.id,
                contact_id_first.contact[0]
            )
            model_asset_contacts = self.api_es_assets.get_valid_contact_for_asset_by_id(
                model_asset.id,
                contact_id_first.contact[0]
            )
            assert model_asset_contacts.fullName == model_contact_first.fullName, \
                f'Expected {model_asset_contacts.fullName}, but got {model_contact_first.fullName}.'
            assert model_asset_contacts.description == model_contact_first.description, \
                f'Expected {model_asset_contacts.description}, but got {model_contact_first.description}.'
            assert model_asset_contacts.position == model_contact_first.position, \
                f'Expected {model_asset_contacts.position}, but got {model_contact_first.position}.'
            assert model_asset_contacts.email == model_contact_first.email, \
                f'Expected {model_asset_contacts.email}, but got {model_contact_first.email}.'
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_mass_contacts(contact_id_first.contact[0])

    @allure.title('Test delete contact person from asset by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23962")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23962)
    def test_delete_contact_person_from_asset_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contact_id_first = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_assets.post_add_contact_persons_for_asset(
                model_asset.id,
                contact_id_first.contact[0]
            )
            self.api_es_assets.delete_contact_person_from_asset_by_id(
                model_asset.id,
                contact_id_first.contact[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_mass_contacts(contact_id_first.contact[0])

    @allure.title('Test delete contact persons from asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23964")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23964)
    def test_delete_contact_persons_from_asset_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        contact_id_first = self.api_common_contacts.post_add_contacts()
        contact_id_second = self.api_common_contacts.post_add_contacts()
        contact_id_third = self.api_common_contacts.post_add_contacts()
        try:
            self.api_es_assets.post_add_contact_persons_for_asset(
                model_asset.id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
            self.api_es_assets.delete_contact_persons_from_asset_by_list(
                model_asset.id,
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_common_contacts.delete_mass_contacts(
                contact_id_first.contact[0],
                contact_id_second.contact[0],
                contact_id_third.contact[0]
            )

    @allure.title('Test update assets by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23969")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23969)
    def test_put_update_assets_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        company_id_second = self.api_es_companies.post_add_our_company()
        location_id_second = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id_second,
            location_id=location_id_second
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_asset_first = self.api_es_assets.get_detailed_information_on_object_by_id(model_asset.id)
        try:
            self.api_es_assets.put_update_assets_by_list(model_asset.id, company_id=company_id_second)
            model_asset_updated = self.api_es_assets.get_detailed_information_on_object_by_id(model_asset.id)
            assert model_asset_first.isMobileAsset != model_asset_updated.isMobileAsset, \
                f'{model_asset_first.isMobileAsset} is equal {model_asset_updated.isMobileAsset}'
            assert model_asset_first.company.id != model_asset_updated.company.id, \
                f'{model_asset_first.company.id} is equal {model_asset_updated.company.id}'
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_companies.delete_company_by_id(company_id_second)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_es_locations.delete_location_by_id(location_id_second)

    @allure.title('Test delete assets by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23971")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23971)
    def test_delete_assets_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_asset_second = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_asset_third = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assets.delete_assets_by_list(
                model_asset.id,
                model_asset_second.id,
                model_asset_third.id
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test returns the header of a user query with the amount of data that satisfies the filter.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23973")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23973)
    def test_head_assets(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_es_assets.post_add_checklist_to_asset_by_id(model_asset.id, model_checklist.result[0])
        district_id = self.api_es_districts.post_add_district()
        self.api_es_asset_districts.add_district_to_object(
            asset_id=model_asset.id,
            district_id=district_id.districts[0]
        )
        try:
            self.api_es_assets.head_assets(
                asset_id=model_asset.id,
                checklist_id=model_checklist.result[0],
                district_id=district_id.districts[0],
                company_id=company_id
            )
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
            self.api_es_districts.delete_district_by_id(district_id.districts[0])

    @allure.title('Test method of unpublishing of an asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23984")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23984)
    def test_put_method_of_unpublishing_asset_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=model_asset.id,
            work_type_id=work_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=model_asset.id,
            location_id=location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(model_asset.id)
        try:
            self.api_es_assets.put_method_of_unpublishing_asset_by_id(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete the asset and all child assets by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23988")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23988)
    def test_delete_asset_and_child_assets_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset_parent = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assetlocations.add_location_to_object(
                asset_id=model_asset_parent.id,
                location_id=location_id
            )
            self.api_es_assets.post_add_asset_with_parent(
                parent_id=model_asset_parent.id,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id
            )
            self.api_es_assets.delete_asset_and_child_assets_by_id(model_asset_parent.id)
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete the assets and all child assets by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23989")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23989)
    def test_delete_assets_and_child_assets_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        location_id_second = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset_parent = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_asset_parent_second = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assetlocations.add_location_to_object(
                asset_id=model_asset_parent.id,
                location_id=location_id
            )
            self.api_es_assetlocations.add_location_to_object(
                asset_id=model_asset_parent_second.id,
                location_id=location_id_second
            )
            self.api_es_assets.post_add_asset_with_parent(
                parent_id=model_asset_parent.id,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id
            )
            self.api_es_assets.post_add_asset_with_parent(
                parent_id=model_asset_parent_second.id,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id
            )
            self.api_es_assets.delete_assets_and_child_assets_by_list(
                model_asset_parent.id,
                model_asset_parent_second.id
            )
        finally:
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id, location_id_second)

    @allure.title('Test restores deleted assets by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23992")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23992)
    def test_put_restores_deleted_assets_by_list(self):
        try:
            model_deleted_assets = self.api_es_assets.get_asset_available_to_user(
                {"isDeleted": True},
                None
            )
            list_assets_id = [int(key) for key in model_deleted_assets.results.keys()]
            self.api_es_assets.put_restores_deleted_assets_by_list(*list_assets_id)
            self.api_es_assets.delete_assets_by_list(*list_assets_id)
        except (AssertionError, TypeError, Exception, ValueError):
            company_id = self.api_es_companies.post_add_our_company()
            location_id = self.api_es_locations.post_add_location()
            self.api_es_company_locations.post_add_company_locations(
                company_id=company_id,
                location_id=location_id
            )
            asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
            asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
            model_asset = self.api_es_assets.post_add_object(
                company_id=company_id,
                asset_class_id=asset_class_id,
                asset_type_id=asset_type_id
            )
            model_asset_second = self.api_es_assets.post_add_object(
                company_id=company_id,
                asset_class_id=asset_class_id,
                asset_type_id=asset_type_id
            )
            try:
                self.api_es_assets.delete_assets_by_list(
                    model_asset.id,
                    model_asset_second.id
                )
                self.api_es_assets.put_restores_deleted_assets_by_list(model_asset.id, model_asset_second.id)
            finally:
                self.api_es_assets.delete_assets_by_list(
                    model_asset.id,
                    model_asset_second.id
                )
                self.api_es_companies.delete_company_by_id(company_id)
                self.api_es_locations.delete_locations_by_list(location_id)

    @allure.title('Test get the list of districts for the asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23997")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23997)
    def test_get_list_districts_for_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_districts = self.api_es_districts.post_add_three_districts()
        try:
            self.api_es_asset_districts.add_districts_to_asset(
                model_asset.id,
                *model_districts.districts
            )
            self.api_es_assets.get_list_districts_for_asset(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)
            self.api_es_districts.delete_districts_by_list(*model_districts.districts)

    @allure.title('Test get a list of active (not deleted) tags by asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23999")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23999)
    def test_get_actual_locations_of_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_assetlocations.add_location_to_object(
                asset_id=model_asset.id,
                location_id=location_id
            )
            self.api_es_assets.get_actual_locations_of_asset(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)

    @allure.title('Test get a list of the asset skills.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24007")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24007)
    def test_get_list_skill_of_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_skills = self.api_pa_skills.post_add_three_skills_to_tenant()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )

        try:
            self.api_es_asset_skills.post_add_skills_to_one_asset(
                model_asset.id,
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )
            self.api_es_assets.get_list_skill_of_asset(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)
            self.api_pa_skills.delete_skills_by_list(
                model_skills.skills[0].skillID,
                model_skills.skills[1].skillID,
                model_skills.skills[2].skillID
            )

    @allure.title('Test get a list of active (not deleted) tags by asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24018")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24018)
    def test_get_list_active_tags_by_asset(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        try:
            self.api_es_asset_tags.post_add_tags_to_asset(model_asset.id)
            self.api_es_assets.get_list_active_tags_by_asset(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)

    @allure.title('Test get a list of work types available for the asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24020")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24020)
    def test_get_list_asset_work_types(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        model_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=model_asset.id,
            work_type_id=work_type_id
        )
        try:
            self.api_es_assets.get_list_asset_work_types(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_locations_by_list(location_id)


@pytest.mark.test_scripts_suites_es_assets
class TestEsAssetsScriptSuite(BaseTest):

    @allure.title('Test api test script ES/assets (POST, GET, GET by id, DELETE by id, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24540")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24540)
    @pytest.mark.test_script_runs
    def test_es_asset_add_get_delete_by_id_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    self.api_es_assets.get_asset_available_to_user({"isDeleted": "false"}, object_model)
                    self.api_es_assets.get_asset_by_id(object_model, None)
                    self.api_es_assets.delete_object_by_id(object_model.id)
                    self.api_es_assets.get_asset_available_to_user({"isDeleted": "true"}, object_model)
                    self.api_es_assets.get_asset_by_id(object_model, True)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (POST, GET, GET by id, DELETE by list, GET, GET by id) .')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24541")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24541)
    @pytest.mark.test_script_runs
    def test_es_asset_add_get_delete_by_list_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    self.api_es_assets.get_asset_available_to_user({"isDeleted": "false"}, object_model)
                    self.api_es_assets.get_asset_by_id(object_model, None)
                    self.api_es_assets.delete_assets_by_list(object_model.id)
                    self.api_es_assets.get_asset_available_to_user({"isDeleted": "true"}, object_model)
                    self.api_es_assets.get_asset_by_id(object_model, True)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (DELETE by id full, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24542")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24542)
    @pytest.mark.test_script_runs
    def test_es_asset_delete_by_id_full_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    model_child_asset = self.api_es_assets.post_add_child_asset(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id,
                        parent_id=object_model.id
                    )
                    self.api_es_assets.delete_asset_and_child_assets_by_id(object_model.id)
                    self.api_es_assets.get_asset_available_to_user(
                        {"isDeleted": "true"},
                        object_model,
                        model_child_asset
                    )
                    self.api_es_assets.get_asset_by_id(object_model, True)
                    self.api_es_assets.get_asset_by_id(model_child_asset, True)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (DELETE by list full, GET, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24543")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24543)
    @pytest.mark.test_script_runs
    def test_es_asset_delete_by_list_full_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    model_child_asset = self.api_es_assets.post_add_child_asset(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id,
                        parent_id=object_model.id
                    )
                    self.api_es_assets.delete_assets_and_child_assets_by_list(object_model.id)
                    self.api_es_assets.get_asset_available_to_user(
                        {"isDeleted": "true"},
                        object_model,
                        model_child_asset
                    )
                    self.api_es_assets.get_asset_by_id(object_model, True)
                    self.api_es_assets.get_asset_by_id(model_child_asset, True)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (DELETE by id, PUT restore, GET by list, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24544")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24544)
    @pytest.mark.test_script_runs
    def test_es_asset_delete_by_id_put_restore_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    self.api_es_assets.delete_object_by_id(object_model.id)
                    self.api_es_assets.put_restores_deleted_assets_by_list(object_model.id)
                    self.api_es_assets.get_asset_available_to_user(
                        {"isDeleted": "false"},
                        object_model
                    )
                    self.api_es_assets.get_asset_by_id(object_model, False)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
                finally:
                    self.api_es_assets.delete_object_by_id(object_model.id)

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (DELETE by list, PUT restore, GET by list, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24545")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24545)
    @pytest.mark.test_script_runs
    def test_es_asset_delete_by_list_put_restore_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    self.api_es_assets.delete_assets_by_list(object_model.id)
                    self.api_es_assets.put_restores_deleted_assets_by_list(object_model.id)
                    self.api_es_assets.get_asset_available_to_user(
                        {"isDeleted": "false"},
                        object_model
                    )
                    self.api_es_assets.get_asset_by_id(object_model, False)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
                finally:
                    self.api_es_assets.delete_object_by_id(object_model.id)

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (DELETE by id full, PUT restore, GET by list, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24546")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24546)
    @pytest.mark.test_script_runs
    def test_es_asset_delete_by_id_full_put_restore_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    model_child_asset = self.api_es_assets.post_add_child_asset(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id,
                        parent_id=object_model.id
                    )
                    self.api_es_assets.delete_asset_and_child_assets_by_id(object_model.id)
                    self.api_es_assets.put_restores_deleted_assets_by_list(object_model.id, model_child_asset.id)
                    self.api_es_assets.get_asset_available_to_user(
                        {"isDeleted": "false"},
                        object_model,
                        model_child_asset
                    )
                    self.api_es_assets.get_asset_by_id(object_model, False)
                    self.api_es_assets.get_asset_by_id(model_child_asset, False)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
                finally:
                    self.api_es_assets.delete_assets_by_list(object_model.id, model_child_asset.id)

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets (DELETE by list full, PUT restore, GET by list, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24547")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id(24547)
    @pytest.mark.test_script_runs
    def test_es_asset_delete_by_list_full_put_restore_get_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()

        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    object_model = self.api_es_assets.post_add_object(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id
                    )
                    model_child_asset = self.api_es_assets.post_add_child_asset(
                        company_id=company_id,
                        asset_class_id=asset_class_id,
                        asset_type_id=asset_type_id,
                        parent_id=object_model.id
                    )
                    self.api_es_assets.delete_assets_and_child_assets_by_list(object_model.id)
                    self.api_es_assets.put_restores_deleted_assets_by_list(object_model.id, model_child_asset.id)
                    self.api_es_assets.get_asset_available_to_user(
                        {"isDeleted": "false"},
                        object_model,
                        model_child_asset
                    )
                    self.api_es_assets.get_asset_by_id(object_model, False)
                    self.api_es_assets.get_asset_by_id(model_child_asset, False)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
                finally:
                    self.api_es_assets.delete_assets_by_list(object_model.id, model_child_asset.id)

        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)

    @allure.title('Test api test script ES/assets/avatar (PUT from form, GET by id, DELETE, GET by id).')
    @allure.severity(Severity.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.test_task_id(24511)
    @pytest.mark.test_case_id()
    @pytest.mark.test_script_runs
    def test_es_asset_avatar_put_from_form_get_by_id_delete_get_by_id(self, request, return_func_name):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        runs = int(request.config.getoption("--runs"))
        errors = []

        for i in range(runs):
            with (allure.step(f"Run #[{i+1}]")):
                try:
                    model_avatar = self.api_es_assets.put_upload_avatar_for_asset_data_from_form(object_model.id)
                    self.api_es_assets.get_asset_by_id_avatar(object_model.id, model_avatar, False)
                    self.api_es_assets.delete_avatar_from_asset_by_id(object_model.id)
                    self.api_es_assets.get_asset_by_id_avatar(object_model.id, model_avatar, True)
                except (AssertionError, JSONDecodeError) as e:
                    logger.error(f"Error in Run #[{i+1}]: {e}")
                    name = return_func_name()
                    errors.append(f"Run #[{i + 1}] - {name} FAILED - {str(e)}")
                finally:
                    self.api_common_attachments.delete_attachment_by_id(model_avatar.attachmentID)

        self.api_es_assets.delete_assets_by_list(object_model.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

        if errors:
            pytest.fail(f"The test encountered errors:\n" + "\n".join(errors), pytrace=False)
