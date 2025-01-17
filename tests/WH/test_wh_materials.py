import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWhMaterials(BaseTest):

    @allure.title('Test add materials.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24497")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на создание материала проходит в - test_delete_materials_by_list")
    @pytest.mark.test_case_id(24497)
    def test_post_add_materials(self):
        self.api_wh_materials.post_add_materials(None)

    @allure.title('Test delete materials by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24498")
    @pytest.mark.regress
    @pytest.mark.skip(reason="Тест на удаление материала проходит в - test_get_material_by_id")
    @pytest.mark.test_case_id(24498)
    def test_delete_materials_by_list(self):
        model_materials = self.api_wh_materials.post_add_materials(None)
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])

    @allure.title('Test get material by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24507")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24507)
    def test_get_material_by_id(self):
        model_materials = self.api_wh_materials.post_add_materials(None)
        self.api_wh_materials.get_material_by_id(model_materials.result[0])
        self.api_wh_materials.delete_materials_by_list(model_materials.result[0])
