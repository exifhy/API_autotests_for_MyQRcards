import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsAssetSchemas(BaseTest):

    @allure.title('Test add plan-scheme only name.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24083")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24083)
    def test_post_add_asset_scheme_only_name(self):
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
            self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete the asset-scheme by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24087")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24087)
    def test_delete_asset_scheme_by_id(self):
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
            model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get a list of asset schemes available to the user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24090")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24090)
    def test_get_list_asset_schemes_available_to_user(self):
        self.api_es_asset_schemas.get_list_asset_schemes_available_to_user()

    @allure.title('Test update the plan-schemes, change name scheme.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24088")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24088)
    def test_put_update_asset_scheme(self):
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
            model_scheme_before = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
            model_scheme_after = self.api_es_asset_schemas.put_update_asset_scheme(
                model_asset.id,
                model_scheme_before.id
            )
            assert model_scheme_before.name != model_scheme_after.name, \
                f'{model_scheme_before.name} is equal {model_scheme_after.name}.'
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme_after.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get the asset scheme attached to the asset.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24084")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24084)
    def test_get_asset_scheme_attached_to_asset(self):
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
            model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
            model_get_scheme = self.api_es_asset_schemas.get_asset_scheme_attached_to_asset(model_asset.id)
            assert model_scheme.name == model_get_scheme.name, \
                f'Expected {model_scheme.name}, but got {model_get_scheme.name}'
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get a list of existing asset-scheme for the current asset and all available asset up the tree.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24085")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24085)
    def test_get_asc_list_asset_scheme_for_asset(self):
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
            model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
            self.api_es_asset_schemas.get_asc_list_asset_scheme_for_asset(model_asset.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get the asset-scheme by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24086")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24086)
    def test_get_plan_scheme_by_id(self):
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
            model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
            self.api_es_asset_schemas.get_plan_scheme_by_id(model_scheme.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
        finally:
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test bind asset schemes to asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24091")
    @pytest.mark.skip(reason="Тест на привязку плана проходит в - test_put_unbind_asset_schemes_from_asset_by_list")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24091)
    def test_post_bind_asset_schemes_to_asset_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset_first = self.api_es_assets.post_add_object(
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
            model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset_first.id)
            self.api_es_asset_schemas.post_bind_asset_schemes_to_asset_by_list(
                model_scheme.id,
                model_asset_second.id,
                model_asset_third.id
            )
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
        finally:
            self.api_es_assets.delete_assets_by_list(
                model_asset_first.id,
                model_asset_second.id,
                model_asset_third.id
            )
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test unbind asset schemes from asset by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24092")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24092)
    def test_put_unbind_asset_schemes_from_asset_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset_first = self.api_es_assets.post_add_object(
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
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset_first.id)
        try:
            self.api_es_asset_schemas.post_bind_asset_schemes_to_asset_by_list(
                model_scheme.id,
                model_asset_second.id,
                model_asset_third.id
            )
            self.api_es_asset_schemas.put_unbind_asset_scheme_from_assets_by_list(
                model_scheme.id,
                model_asset_first.id,
                model_asset_second.id,
                model_asset_third.id
            )
        finally:
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_assets_by_list(
                model_asset_first.id,
                model_asset_second.id,
                model_asset_third.id
            )
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test upload file to server and bind to asset scheme, data from form.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24098")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24098)
    def test_post_upload_file_to_server_and_bind_asset_scheme_data_from_form(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        model_asset_first = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset_first.id)
        try:
            self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
        finally:
            self.api_es_asset_schemas.delete_picture_associated_with_asset_scheme(model_scheme.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(model_asset_first.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test method to get TemporaryRedirect to a temporary link for downloading the attached plan file.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24097")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24097)
    def test_get_temporary_link_for_downloading_attached_plan_file(self):
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
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
        try:
            self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
            self.api_es_asset_schemas.get_temporary_link_for_downloading_attached_plan_file(model_scheme.id)
        finally:
            self.api_es_asset_schemas.delete_picture_associated_with_asset_scheme(model_scheme.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test bind attachment to asset scheme if attachment upload from common service.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24093")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24093)
    def test_post_bind_attachment_to_asset_scheme(self):
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
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
        try:
            attachment = self.api_common_attachments.post_upload_attachments_to_server_data_from_form()
            self.api_es_asset_schemas.post_bind_attachment_to_asset_scheme(
                model_scheme.id,
                attachment.attachmentID
            )
        finally:
            self.api_es_asset_schemas.delete_picture_associated_with_asset_scheme(model_scheme.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test gets information about the picture attached to the asset-scheme.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24094")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24094)
    def test_get_info_picture_attached_to_asset_scheme(self):
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
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
        try:
            self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
            self.api_es_asset_schemas.get_info_picture_attached_to_asset_scheme(model_scheme.id)
        finally:
            self.api_es_asset_schemas.delete_picture_associated_with_asset_scheme(model_scheme.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete the current view (picture) associated with the asset-scheme.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24096")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24096)
    def test_delete_picture_associated_with_asset_scheme(self):
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
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(model_asset.id)
        try:
            self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
            self.api_es_asset_schemas.delete_picture_associated_with_asset_scheme(model_scheme.id)
        finally:
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(model_asset.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test adds points to the asset scheme.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24103")
    @pytest.mark.skip(reason='Тест добавления точки на схему проходит в - test_delete_points_from_asset_schema_by_list')
    @pytest.mark.regress
    @pytest.mark.test_case_id(24103)
    def test_post_add_points_to_asset_schema(self):
        district_id = self.api_es_districts.post_add_district()
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_districts.add_district_to_object(asset_id=object_model.id,
                                                           district_id=district_id.districts[0])
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(object_model.id)
        self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            self.api_es_asset_schemas.post_add_points_to_asset_schema(model_scheme.id, model_task.id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id=district_id.districts[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete points from the asset scheme by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24104")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24104)
    def test_delete_points_from_asset_schema_by_list(self):
        district_id = self.api_es_districts.post_add_district()
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_districts.add_district_to_object(asset_id=object_model.id,
                                                           district_id=district_id.districts[0])
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(object_model.id)
        self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            model_points = self.api_es_asset_schemas.post_add_points_to_asset_schema(model_scheme.id, model_task.id)
            self.api_es_asset_schemas.delete_points_from_asset_schema_by_list(
                model_scheme.id,
                model_points.result[0].pointID
            )
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id=district_id.districts[0])
            self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get the complete list of task points placed on the asset scheme.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24101")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24101)
    def test_get_list_points_from_asset_schema(self):
        district_id = self.api_es_districts.post_add_district()
        created_location_id = self.api_es_locations.post_add_location()
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        self.api_es_company_locations.post_add_company_locations(
            company_id=company_id,
            location_id=location_id
        )
        asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
        asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
        object_model = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        self.api_es_asset_districts.add_district_to_object(asset_id=object_model.id,
                                                           district_id=district_id.districts[0])
        model_scheme = self.api_es_asset_schemas.post_add_asset_scheme_only_name(object_model.id)
        self.api_es_asset_schemas.post_upload_file_to_server_and_bind_asset_scheme_data_from_form(model_scheme.id)
        self.api_es_asset_work_types.post_add_work_type_to_asset(
            asset_id=object_model.id,
            work_type_id=work_type_id
        )
        self.api_es_assetlocations.add_location_to_object(
            asset_id=object_model.id,
            location_id=created_location_id
        )
        self.api_es_assets.put_method_of_publishing_an_object_by_id(object_model.id)
        criticality_id = self.api_sla_criticalities.get_list_criticalities_return_first_id()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task = self.api_work_tasks.post_add_task(
            criticality_id=criticality_id,
            task_type_id=task_type_id[0],
            asset_id=object_model.id,
            work_type_id=work_type_id,
            company_id=company_id
        )
        try:
            self.api_es_asset_schemas.post_add_points_to_asset_schema(model_scheme.id, model_task.id)
            self.api_es_asset_schemas.get_list_points_from_asset_schema(model_scheme.id)
        finally:
            self.api_work_tasks.delete_task_by_id(model_task.id)
            self.api_es_asset_schemas.delete_asset_scheme_by_id(model_scheme.id)
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_districts.delete_district_by_id(district_id=district_id.districts[0])
            self.api_es_locations.delete_location_by_id(location_id)
