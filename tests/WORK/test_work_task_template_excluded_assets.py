import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskTemplateExcludedAssets(BaseTest):

    @allure.title('Test add task template excluded assets.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25252")
    @pytest.mark.skip(reason="Тест на добавление исключенные объекты к плановой "
                             "заявке проходит в - test_delete_task_template_excluded_assets")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25252)
    def test_post_task_template_excluded_assets(self):
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
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_assets_by_list(
            model_asset.id,
            model_excluded_asset1.id,
            model_excluded_asset2.id
        )
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)

    @allure.title('Test delete task template excluded assets.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25253")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25253)
    def test_delete_task_template_excluded_assets(self):
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
        self.api_work_task_template_excluded_assets.delete_task_template_excluded_assets(
            model_task_templates.templates[0],
            model_excluded_asset1.id,
            model_excluded_asset2.id
        )
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_es_assets.delete_assets_by_list(
            model_asset.id,
            model_excluded_asset1.id,
            model_excluded_asset2.id
        )
        self.api_es_companies.delete_company_by_id(company_id)
        self.api_es_locations.delete_location_by_id(location_id)
