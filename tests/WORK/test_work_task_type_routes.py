import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Work service offers various methods for managing tasks and their corresponding attributes.")
class TestWorkTaskTypeRoutes(BaseTest):

    @allure.title('Test creates routes of task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25324")
    @pytest.mark.skip(reason="Тест на создание маршрута типа заявки проходит в - test_delete_task_types_routes_by_id")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25324)
    def test_post_add_task_types_routes(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task_type_route = self.api_work_task_types.get_route_task_type(int(task_type_id[0]))
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_type_routes.post_add_task_types_routes(
            task_type_id=model_task_type.results[0],
            start_task_stage_id=model_task_type_route.startTaskStage.id,
            start_task_status_id=str(model_task_type_route.startTaskStatus.id),
            finish_task_stage_id=model_task_type_route.finishTaskStage.id
        )
        self.api_work_task_type_routes.delete_task_types_routes_by_list(model_task_type.results[0])
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test delete routes task types by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25333")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25333)
    def test_delete_task_types_routes_by_id(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task_type_route = self.api_work_task_types.get_route_task_type(int(task_type_id[0]))
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_type_routes.post_add_task_types_routes(
            task_type_id=model_task_type.results[0],
            start_task_stage_id=model_task_type_route.startTaskStage.id,
            start_task_status_id=str(model_task_type_route.startTaskStatus.id),
            finish_task_stage_id=model_task_type_route.finishTaskStage.id
        )
        self.api_work_task_type_routes.delete_task_types_routes_by_id(model_task_type.results[0])
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test delete routes task types by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25332")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25332)
    def test_delete_task_types_routes_by_list(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task_type_route = self.api_work_task_types.get_route_task_type(int(task_type_id[0]))
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_type_routes.post_add_task_types_routes(
            task_type_id=model_task_type.results[0],
            start_task_stage_id=model_task_type_route.startTaskStage.id,
            start_task_status_id=str(model_task_type_route.startTaskStatus.id),
            finish_task_stage_id=model_task_type_route.finishTaskStage.id
        )
        self.api_work_task_type_routes.delete_task_types_routes_by_list(model_task_type.results[0])
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])

    @allure.title('Test update routes task types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25327")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25327)
    def test_put_update_task_types_routes(self):
        task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
        model_task_type_route = self.api_work_task_types.get_route_task_type(int(task_type_id[0]))
        model_task_type = self.api_work_task_types.post_add_task_types()
        self.api_work_task_type_routes.post_add_task_types_routes(
            task_type_id=model_task_type.results[0],
            start_task_stage_id=model_task_type_route.startTaskStage.id,
            start_task_status_id=str(model_task_type_route.startTaskStatus.id),
            finish_task_stage_id=model_task_type_route.finishTaskStage.id
        )
        model_task_type_route_before = self.api_work_task_types.get_route_task_type(model_task_type.results[0])
        self.api_work_task_type_routes.put_update_task_types_routes(
            task_type_id=model_task_type.results[0],
            start_task_stage_id=model_task_type_route.finishTaskStage.id,
            start_task_status_id=model_task_type_route.startTaskStatus.id,
            finish_task_stage_id=model_task_type_route.startTaskStage.id
        )
        model_task_type_route_after = self.api_work_task_types.get_route_task_type(model_task_type.results[0])
        assert model_task_type_route_before.startTaskStage.id != model_task_type_route_after.startTaskStage.id, \
            f"{model_task_type_route_before.startTaskStage.id} is equal {model_task_type_route_after.startTaskStage.id}"
        assert model_task_type_route_before.finishTaskStage.id != model_task_type_route_after.finishTaskStage.id, \
            f"{model_task_type_route_before.finishTaskStage.id} is equal {model_task_type_route_after.finishTaskStage.id}"
        self.api_work_task_type_routes.delete_task_types_routes_by_id(model_task_type.results[0])
        self.api_work_task_types.delete_task_types_by_id(model_task_type.results[0])


