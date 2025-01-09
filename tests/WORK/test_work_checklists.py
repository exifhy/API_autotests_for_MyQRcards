import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkChecklists(BaseTest):

    @allure.title('Test add checklists.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23908")
    @pytest.mark.skip(reason="Тест на создание чек-листа проходит в - test_delete_checklist_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23908)
    def test_post_add_checklists(self):
        self.api_work_checklists.post_add_checklists()

    @allure.title('Test delete checklist by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23910")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23910)
    def test_delete_checklist_by_id(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test get checklist by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23942")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23942)
    def test_get_checklist_by_id(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        try:
            self.api_work_checklists.get_checklist_by_id(model_checklist.result[0])
        finally:
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test delete checklists by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23944")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23944)
    def test_delete_checklists_by_list(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        model_checklist_second = self.api_work_checklists.post_add_checklists()
        model_checklist_third = self.api_work_checklists.post_add_checklists()
        self.api_work_checklists.delete_checklist_by_list(
            model_checklist.result[0],
            model_checklist_second.result[0],
            model_checklist_third.result[0],
        )

    @allure.title('Test get list checklists.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24324")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24324)
    def test_get_list_checklists(self):
        self.api_work_checklists.get_list_checklists()

    @allure.title('Test update checklist by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24325")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24325)
    def test_get_checklist_by_id(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        checklist_before = self.api_work_checklists.get_checklist_by_id(model_checklist.result[0])
        try:
            self.api_work_checklists.put_update_checklists(model_checklist.result[0])
            checklist_after = self.api_work_checklists.get_checklist_by_id(model_checklist.result[0])
            assert checklist_before != checklist_after, f'{checklist_before} is equal {checklist_after}'
        finally:
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test assign checklist to asset and work type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24326")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24326)
    def test_post_checklist_assign(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        model_checklist = self.api_work_checklists.post_add_checklists()
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
        try:
            self.api_work_checklists.post_checklists_assign(
                model_checklist.result[0],
                object_model.id,
                work_type_id
            )
        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test delete assign checklist from asset and work type.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24327")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24327)
    def test_delete_checklist_assign(self):
        company_id = self.api_es_companies.post_add_our_company()
        created_location_id = self.api_es_locations.post_add_location()
        model_checklist = self.api_work_checklists.post_add_checklists()
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
        try:
            self.api_work_checklists.post_checklists_assign(
                model_checklist.result[0],
                object_model.id,
                work_type_id
            )
            self.api_work_checklists.delete_checklists_assign(
                model_checklist.result[0],
                object_model.id,
                work_type_id
            )

        finally:
            self.api_es_assets.delete_object_by_id(object_model.id)
            self.api_es_companies.delete_company_by_id(company_id)
            self.api_es_locations.delete_location_by_id(created_location_id)
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])

    @allure.title('Test get items checklist by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24328")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24328)
    def test_get_checklist_items_by_id(self):
        model_checklist = self.api_work_checklists.post_add_checklists()
        self.api_work_checklist_items.post_add_checklist_items(model_checklist.result[0])
        try:
            self.api_work_checklists.get_checklist_items_by_id(model_checklist.result[0])
        finally:
            self.api_work_checklists.delete_checklist_by_id(model_checklist.result[0])
