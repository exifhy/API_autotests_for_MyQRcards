import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskTemplates(BaseTest):

    # @allure.title('Test add task templates.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23296")
    # @pytest.mark.skip(reason="Тест на создание шаблона заявки проходит в - test_delete_task_templates_by_id")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(23296)
    # def test_post_add_task_templates(self):
    #     company_id = self.api_es_companies.post_add_our_company()
    #     location_id = self.api_es_locations.post_add_location()
    #     task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
    #     work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
    #     self.api_es_company_locations.post_add_company_locations(
    #         company_id=company_id,
    #         location_id=location_id
    #     )
    #     asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
    #     asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
    #     model_asset = self.api_es_assets.post_add_object(
    #         company_id=company_id,
    #         asset_class_id=asset_class_id,
    #         asset_type_id=asset_type_id
    #     )
    #     model_task_templates = self.api_work_task_templates.post_add_task_templates(
    #         model_asset.id,
    #         str(task_type_id[0]),
    #         str(work_type_id)
    #     )
    #     self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
    #     self.api_es_assets.delete_object_by_id(model_asset.id)
    #     self.api_es_companies.delete_company_by_id(company_id)
    #     self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete task templates by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23313")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23313)
    def test_delete_task_templates_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get task template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25233")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25233)
    def test_get_task_template_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.get_task_template_by_id(model_task_templates.templates[0])
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test update task template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25234")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25234)
    def test_put_update_task_templates(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.put_update_task_templates(
            model_task_templates.templates[0],
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test head task template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25236")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25236)
    def test_head_task_templates(self):
        self.api_work_task_templates.head_task_templates()

    @allure.title('Test get download qr code task template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25237")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25237)
    def test_get_download_qr_code_task_templates(self):
        self.api_work_task_templates.get_download_qr_code_task_templates()

    @allure.title('Test get download qr code by task template ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25238")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25238)
    def test_get_download_qr_code_task_template_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.get_download_qr_code_task_template_by_id(model_task_templates.templates[0])
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    # @allure.title('Test publishes task template by ID.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25239")
    # @pytest.mark.skip(reason="Тест публикации шаблона заявки проходит в - test_put_unpublish_task_template_by_id")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25239)
    # def test_put_publish_task_template_by_id(self):
    #     company_id = self.api_es_companies.post_add_our_company()
    #     location_id = self.api_es_locations.post_add_location()
    #     task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
    #     work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
    #     self.api_es_company_locations.post_add_company_locations(
    #         company_id=company_id,
    #         location_id=location_id
    #     )
    #     asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
    #     asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
    #     model_asset = self.api_es_assets.post_add_object(
    #         company_id=company_id,
    #         asset_class_id=asset_class_id,
    #         asset_type_id=asset_type_id
    #     )
    #     model_task_templates = self.api_work_task_templates.post_add_task_templates(
    #         model_asset.id,
    #         str(task_type_id[0]),
    #         str(work_type_id)
    #     )
    #     public_template = self.api_work_task_templates.put_publish_task_template(model_task_templates.templates[0])
    #     self.api_work_task_templates.put_unpublish_task_template(public_template.id)
    #     self.api_work_task_templates.delete_task_templates_by_id(public_template.id)
    #     self.api_es_assets.delete_object_by_id(model_asset.id)
    #     self.api_es_companies.delete_company_by_id(company_id)
    #     self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test unpublishes task template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25240")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25240)
    def test_put_unpublish_task_template_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        public_template = self.api_work_task_templates.put_publish_task_template(model_task_templates.templates[0])
        self.api_work_task_templates.put_unpublish_task_template(public_template.id)
        self.api_work_task_templates.delete_task_templates_by_id(public_template.id)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get public task template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25242")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25242)
    def test_get_public_task_template(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        public_template = self.api_work_task_templates.put_publish_task_template(model_task_templates.templates[0])
        self.api_work_task_templates.get_public_task_template(public_template.id)
        self.api_work_task_templates.delete_task_templates_by_id(public_template.id)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test add users to task template by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23308")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23308)
    def test_post_bind_employee_to_template_by_list(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID,
            model_user2.userID
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_adm_users.delete_user_by_id(user_id=model_user2.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list employee from task template by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25244")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25244)
    def test_get_list_users_from_task_template_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID,
            model_user2.userID
        )
        self.api_work_task_templates.get_list_users_from_task_template_by_id(model_task_templates.templates[0])
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_adm_users.delete_user_by_id(user_id=model_user2.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list excluded assets from task template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25246")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25246)
    def test_get_list_excluded_assets_from_task_template(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_excluded_asset1 = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_excluded_asset2 = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_template_excluded_assets.post_task_template_excluded_assets(
            model_task_templates.templates[0],
            model_excluded_asset1.id,
            model_excluded_asset2.id
        )
        model_list_excluded_assets = self.api_work_task_templates.get_list_excluded_assets_from_task_template(
            model_task_templates.templates[0]
        )
        assert str(model_excluded_asset1.id) in model_list_excluded_assets.root, \
            (f'Added excluded asset {model_excluded_asset1.id} not in '
             f'list excluded assets task template {model_task_templates.templates[0]}')
        assert str(model_excluded_asset2.id) in model_list_excluded_assets.root, \
            (f'Added excluded asset {model_excluded_asset2.id} not in '
             f'list excluded assets task template {model_task_templates.templates[0]}')
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_assets_by_list(
            model_asset.id,
            model_excluded_asset1.id,
            model_excluded_asset2.id
        )
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete excluded assets from task template.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25247")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25247)
    def test_delete_excluded_assets_from_task_template_by_asset_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_excluded_asset = self.api_es_assets.post_add_object(
            company_id=company_id,
            asset_class_id=asset_class_id,
            asset_type_id=asset_type_id
        )
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_template_excluded_assets.post_task_template_excluded_assets(
            model_task_templates.templates[0],
            model_excluded_asset.id
        )
        self.api_work_task_templates.delete_excluded_assets_from_task_template_by_asset_id(
            model_task_templates.templates[0],
            model_excluded_asset.id
        )
        model_list_excluded_assets = self.api_work_task_templates.get_list_excluded_assets_from_task_template(
            model_task_templates.templates[0]
        )
        assert model_list_excluded_assets is None, \
            "Excluded assets not deleted from task templete"
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_assets_by_list(
            model_asset.id,
            model_excluded_asset.id
        )
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test add task template for the schedule.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23309")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23309)
    def test_post_add_task_templates_for_schedules_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID
        )
        model_schedule = self.api_pmp_schedules.post_add_schedule()
        self.api_work_task_templates.post_add_task_templates_for_schedules_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get list task template schedule.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25248")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25248)
    def test_get_list_task_templates_schedules(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID
        )
        model_schedule = self.api_pmp_schedules.post_add_schedule()
        self.api_work_task_templates.post_add_task_templates_for_schedules_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.get_list_task_templates_schedules(
            task_templates_id=model_task_templates.templates[0]
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test regeneration of events for schedule.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25249")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25249)
    def test_post_appointments_schedules_task_templates(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID
        )
        model_schedule = self.api_pmp_schedules.post_add_schedule()
        self.api_work_task_templates.post_add_task_templates_for_schedules_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.post_appointments_schedules_task_templates(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    # @allure.title('Test schedule activation by ID.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23310")
    # @pytest.mark.skip(reason="Тест на активацию расписания проходит в - test_put_schedule_deactivation_by_id")
    # @pytest.mark.smoke
    # @pytest.mark.test_case_id(23310)
    # def test_schedule_activation_by_id(self):
    #     company_id = self.api_es_companies.post_add_our_company()
    #     location_id = self.api_es_locations.post_add_location()
    #     task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
    #     work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
    #     self.api_es_company_locations.post_add_company_locations(
    #         company_id=company_id,
    #         location_id=location_id
    #     )
    #     asset_type_id = self.api_es_asset_types.get_list_asset_types_return_is_hostable_true()
    #     asset_class_id = self.api_es_asset_classes.get_list_asset_classes_return_id_first_class()
    #     model_asset = self.api_es_assets.post_add_object(
    #         company_id=company_id,
    #         asset_class_id=asset_class_id,
    #         asset_type_id=asset_type_id
    #     )
    #     model_user = self.api_adm_users.post_add_user_staff()
    #     model_task_templates = self.api_work_task_templates.post_add_task_templates(
    #         model_asset.id,
    #         str(task_type_id[0]),
    #         str(work_type_id)
    #     )
    #     self.api_work_task_templates.post_bind_employee_to_template_by_list(
    #         model_task_templates.templates[0],
    #         model_user.userID
    #     )
    #     model_schedule = self.api_pmp_schedules.post_add_schedule()
    #     self.api_work_task_templates.post_add_task_templates_for_schedules_by_id(
    #         task_templates_id=model_task_templates.templates[0],
    #         schedule_id=model_schedule.schedules[0]
    #     )
    #     self.api_work_task_templates.put_schedule_activation_by_id(
    #         task_templates_id=model_task_templates.templates[0],
    #         schedule_id=model_schedule.schedules[0]
    #     )
    #     self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
    #     self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
    #     self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
    #     self.api_es_assets.delete_object_by_id(model_asset.id)
    #     self.api_es_companies.delete_company_by_id(company_id)
    #     self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test schedule deactivation by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23311")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23311)
    def test_put_schedule_deactivation_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID
        )
        model_schedule = self.api_pmp_schedules.post_add_schedule()
        self.api_work_task_templates.post_add_task_templates_for_schedules_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.put_schedule_activation_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.put_schedule_deactivation_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test get a list of task templates by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23297")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23297)
    def test_get_list_of_task_templates_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        location_id = self.api_es_locations.post_add_location()
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        work_type_id = self.api_work_work_types.get_list_work_type_return_id_first_published_type()
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
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(
            model_asset.id,
            str(task_type_id[0]),
            str(work_type_id)
        )
        self.api_work_task_templates.post_bind_employee_to_template_by_list(
            model_task_templates.templates[0],
            model_user.userID
        )
        model_schedule = self.api_pmp_schedules.post_add_schedule()
        self.api_work_task_templates.post_add_task_templates_for_schedules_by_id(
            task_templates_id=model_task_templates.templates[0],
            schedule_id=model_schedule.schedules[0]
        )
        self.api_work_task_templates.get_list_task_templates_by_id(model_task_templates.templates[0])
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
