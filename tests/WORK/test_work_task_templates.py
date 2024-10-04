import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Actions with the tasks and attributes")
class TestWorkTaskTemplates(BaseTest):

    @allure.title('Test schedule activation by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23296")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23296)
    def test_schedule_activation_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        model_asset = self.api_es_assets.post_add_object(company_id)
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(model_asset.id)
        self.api_work_task_templates.post_bind_employee_to_template_by_id(
            task_templates_id=model_task_templates.templates[0],
            user_id=model_user.userID
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
        self.api_work_task_templates.delete_task_templates_by_id(model_task_templates.templates[0])
        self.api_pmp_schedules.delete_schedule_by_id(schedule_id=model_schedule.schedules[0])
        self.api_adm_users.delete_user_by_id(user_id=model_user.userID)
        self.api_es_assets.delete_object_by_id(model_asset.id)
        self.api_es_companies.delete_company_by_id(company_id)

    @allure.title('Test get a list of task templates by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23297")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23297)
    def test_get_list_of_task_templates_by_id(self):
        company_id = self.api_es_companies.post_add_our_company()
        model_asset = self.api_es_assets.post_add_object(company_id)
        model_user = self.api_adm_users.post_add_user_staff()
        model_task_templates = self.api_work_task_templates.post_add_task_templates(model_asset.id)
        self.api_work_task_templates.post_bind_employee_to_template_by_id(
            task_templates_id=model_task_templates.templates[0],
            user_id=model_user.userID
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
