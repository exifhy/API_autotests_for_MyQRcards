import allure
import pytest
from config.base_test import BaseTest
from datetime import datetime, timezone
from utils.mail_helper import wait_for_email


@allure.epic("Notifications")
@allure.feature("Email Notifications")
class TestEmailNotifications(BaseTest):


    @allure.title("Проверка отправки email оповещения при создании новой заявки")
    @allure.story("Пользователь с ролью Диспетчер получает email при назначении новой заявки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/29838")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(29838)
    def test_email_notification_on_task_creation(self, email_check_start_time):
        model_user = self.api_adm_users.post_add_user_staff_for_notifications()
        model_rec_rules = None
        model_trigger = None
        model_task = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, role_id)
            model_rec_rules = self.api_msg_recipient_selection_rules.post_recipient_selection_rules(role_id)
            self.api_adm_role_permissions_ext.post_role_permissions_ext_all_task(role_id)
            self.api_adm_role_permissions_ui.post_role_permissions_ui_all_task(role_id, "2")
            model_msg_templates = self.api_msg_message_templates.get_message_templates()
            msg_template_id = next(
                (template.id for template in model_msg_templates.root.values() if template.description == "Новая заявка"),
                None
            )
            model_providers = self.api_msg_providers.get_list_providers()
            provider_id = next(
                (provider.id for provider in model_providers.root.values() if provider.code == "Email"),
                None
            )
            self.api_msg_message_templates.put_update_message_templates_email_create_task(msg_template_id, provider_id)
            model_events = self.api_common_events.get_list_events()
            event_id = next((item.id for item in model_events.root.values() if item.name == "Создана новая заявка"), None)
            model_trigger = self.api_msg_triggers.post_trigger(event_id, msg_template_id)
            self.api_msg_trigger_recipient_selection_rules.post_trigger_recipient_selection_rules(
                model_trigger.results[0], model_rec_rules.results[0]
            )
            task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
            model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
            success, message = wait_for_email(
                model_task.number, email_check_start_time, f"Заявка №{model_task.number}", f"Новая заявка {model_task.number}, по объекту"
                )
            assert success, f"Письмо не прошло проверку или не получено: {message}"
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)

            if model_task:
                self.api_work_tasks.delete_task_by_id(model_task.id)    
            if model_trigger:
                self.api_msg_triggers.delete_trigger_by_id(model_trigger.results[0])
            if model_rec_rules:
                self.api_msg_recipient_selection_rules.delete_recipient_selection_rules(model_rec_rules.results[0])


    @allure.title("Проверка отправки email оповещения при закрытие заявки")
    @allure.story("Пользователь с ролью Диспетчер получает email при закрытие заявки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30354")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30354)
    def test_email_notification_on_task_closed(self, email_check_start_time, bearer_token):
        model_user = self.api_adm_users.post_add_user_staff_for_notifications()
        
        model_rec_rules = None
        model_trigger = None
        model_task = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, role_id)
            model_rec_rules = self.api_msg_recipient_selection_rules.post_recipient_selection_rules(role_id)
            self.api_adm_role_permissions_ext.post_role_permissions_ext_all_task(role_id)
            self.api_adm_role_permissions_ui.post_role_permissions_ui_all_task(role_id, "2")
            model_msg_templates = self.api_msg_message_templates.get_message_templates()
            msg_template_id = next(
                    (template.id for template in model_msg_templates.root.values()
                    if template.description == "Заявка выполнена"
                        and template.subject is not None
                        and "Заявка" in template.subject),
                None
            )
            model_msg_template = self.api_msg_message_templates.get_message_template_by_id(msg_template_id)

            model_providers = self.api_msg_providers.get_list_providers()
            provider_id = next(
                (provider.id for provider in model_providers.root.values() if provider.code == "Email"),
                None
            )
            self.api_msg_message_templates.put_update_message_template(
                msg_template_id,
                model_msg_template.description,
                model_msg_template.subject,
                model_msg_template.content,
                provider_id
                )
            model_events = self.api_common_events.get_list_events()
            event_id = next((item.id for item in model_events.root.values() if item.name == "Заявка закрыта"), None)
            model_trigger = self.api_msg_triggers.post_trigger(event_id, msg_template_id)
            self.api_msg_trigger_recipient_selection_rules.post_trigger_recipient_selection_rules(
                model_trigger.results[0], model_rec_rules.results[0]
            )
            task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
            model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
            self.api_work_tasks.put_task_completed(model_task.id, bearer_token)

            success, message = wait_for_email(
                model_task.number, email_check_start_time, f"Заявка №{model_task.number}", f"Выполнена заявка {model_task.number}, по объекту"
                )
            assert success, f"Письмо не прошло проверку или не получено: {message}"
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            if model_task:
                self.api_work_tasks.delete_task_by_id(model_task.id)    
            if model_trigger:
                self.api_msg_triggers.delete_trigger_by_id(model_trigger.results[0])
            if model_rec_rules:
                self.api_msg_recipient_selection_rules.delete_recipient_selection_rules(model_rec_rules.results[0])


    @allure.title("Проверка отправки email оповещения при изменение заявки")
    @allure.story("Пользователь с ролью Диспетчер получает email при изменение заявки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30355")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30355)
    def test_email_notification_on_task_changed(self, email_check_start_time):
        model_user = self.api_adm_users.post_add_user_staff_for_notifications()
        
        model_rec_rules = None
        model_trigger = None
        model_task = None
        model_msg_template = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, role_id)
            model_rec_rules = self.api_msg_recipient_selection_rules.post_recipient_selection_rules(role_id)
            self.api_adm_role_permissions_ext.post_role_permissions_ext_all_task(role_id)
            self.api_adm_role_permissions_ui.post_role_permissions_ui_all_task(role_id, "2")
            model_providers = self.api_msg_providers.get_list_providers()
            provider_id = next(
                (provider.id for provider in model_providers.root.values() if provider.code == "Email"),
                None
            )
            model_msg_template = self.api_msg_message_templates.post_add_message_template(
                "Заявка №{{ TaskNumber }}",
                "Изменена заявка {{ TaskNumber }}, по объекту {{ AssetFullName }}",
                provider_id
            )
            self.api_msg_message_templates.put_validate_message_templates(model_msg_template.results[0])

            model_events = self.api_common_events.get_list_events()
            
            event_id = next((item.id for item in model_events.root.values() if item.name == "Заявка изменена"), None)

            model_trigger = self.api_msg_triggers.post_trigger(event_id, model_msg_template.results[0])
            self.api_msg_trigger_recipient_selection_rules.post_trigger_recipient_selection_rules(
                model_trigger.results[0], model_rec_rules.results[0]
            )
            task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
            model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
            self.api_work_tasks.patch_update_task_by_id(model_task.id, {"field": "NotesHtml", "value": "<p>Тест</p>"})

            success, message = wait_for_email(
                model_task.number, email_check_start_time, f"Заявка №{model_task.number}", f"Изменена заявка {model_task.number}, по объекту"
                )
            assert success, f"Письмо не прошло проверку или не получено: {message}"
        finally:
            self.api_adm_users.delete_user_by_id(model_user.userID)
            if model_task:
                self.api_work_tasks.delete_task_by_id(model_task.id)    
            if model_trigger:
                self.api_msg_triggers.delete_trigger_by_id(model_trigger.results[0])
            if model_rec_rules:
                self.api_msg_recipient_selection_rules.delete_recipient_selection_rules(model_rec_rules.results[0])
            if model_msg_template:
                self.api_msg_message_templates.delete_message_templates_by_id(model_msg_template.results[0])


    @allure.title("Проверка отправки email оповещения при - изменен пользователь, запросивший заявку")
    @allure.story("Пользователь с ролью Диспетчер получает email при - изменен пользователь, запросивший заявку")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30356")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30356)
    def test_email_notification_on_task_changed_requested_user(self, email_check_start_time):
        model_user = self.api_adm_users.post_add_user_staff_for_notifications()
        
        model_rec_rules = None
        model_trigger = None
        model_task = None
        model_msg_template = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, role_id)
            model_rec_rules = self.api_msg_recipient_selection_rules.post_recipient_selection_rules(role_id)
            self.api_adm_role_permissions_ext.post_role_permissions_ext_all_task(role_id)
            self.api_adm_role_permissions_ui.post_role_permissions_ui_all_task(role_id, "2")
            model_providers = self.api_msg_providers.get_list_providers()
            provider_id = next(
                (provider.id for provider in model_providers.root.values() if provider.code == "Email"),
                None
            )
            model_msg_template = self.api_msg_message_templates.post_add_message_template(
                "Заявка №{{ TaskNumber }}",
                "Изменен пользователь, запросивший заявку {{ TaskNumber }}, по объекту {{ AssetFullName }}",
                provider_id
            )
            self.api_msg_message_templates.put_validate_message_templates(model_msg_template.results[0])

            model_events = self.api_common_events.get_list_events()
            
            event_id = next((item.id for item in model_events.root.values() if item.name == "Изменен пользователь, запросивший заявку"), None)

            model_trigger = self.api_msg_triggers.post_trigger(event_id, model_msg_template.results[0])
            self.api_msg_trigger_recipient_selection_rules.post_trigger_recipient_selection_rules(
                model_trigger.results[0], model_rec_rules.results[0]
            )
            task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
            model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
            self.api_work_tasks.patch_update_task_by_id(model_task.id, {"field": "requestedByUserID", "value": f"{model_user.id}"})

            success, message = wait_for_email(
                model_task.number, email_check_start_time, f"Заявка №{model_task.number}", f"Изменен пользователь, запросивший заявку {model_task.number}, по объекту"
                )
            assert success, f"Письмо не прошло проверку или не получено: {message}"
        finally:
            if model_task:
                self.api_work_tasks.delete_task_by_id(model_task.id)    
            if model_trigger:
                self.api_msg_triggers.delete_trigger_by_id(model_trigger.results[0])
            if model_rec_rules:
                self.api_msg_recipient_selection_rules.delete_recipient_selection_rules(model_rec_rules.results[0])
            if model_msg_template:
                self.api_msg_message_templates.delete_message_templates_by_id(model_msg_template.results[0])
            self.api_adm_users.delete_user_by_id(model_user.userID)


    @allure.title("Проверка отправки email оповещения при - Изменено время по заявке")
    @allure.story("Пользователь с ролью Диспетчер получает email при - Изменено время по заявке")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/30357")
    @pytest.mark.regress
    @pytest.mark.test_case_id(30357)
    def test_email_notification_time_changed_on_task(self, email_check_start_time):
        now_utc = datetime.now(timezone.utc)
        result = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        model_user = self.api_adm_users.post_add_user_staff_for_notifications()
        model_user_second = self.api_adm_users.post_add_user_staff()
        
        model_rec_rules = None
        model_trigger = None
        model_task = None
        model_msg_template = None
        try:
            role_id = self.api_adm_roles.get_list_roles_return_role_id_by_name("Диспетчер")
            self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, role_id)
            model_rec_rules = self.api_msg_recipient_selection_rules.post_recipient_selection_rules(role_id)
            self.api_adm_role_permissions_ext.post_role_permissions_ext_all_task(role_id)
            self.api_adm_role_permissions_ui.post_role_permissions_ui_all_task(role_id, "2")
            model_providers = self.api_msg_providers.get_list_providers()
            provider_id = next(
                (provider.id for provider in model_providers.root.values() if provider.code == "Email"),
                None
            )
            model_msg_template = self.api_msg_message_templates.post_add_message_template(
                "Заявка №{{ TaskNumber }}",
                "Изменено время по заявке {{ TaskNumber }}",
                provider_id
            )
            self.api_msg_message_templates.put_validate_message_templates(model_msg_template.results[0])

            model_events = self.api_common_events.get_list_events()
            
            event_id = next((item.id for item in model_events.root.values() if item.name == "Изменено время по заявке"), None)

            model_trigger = self.api_msg_triggers.post_trigger(event_id, model_msg_template.results[0])
            self.api_msg_trigger_recipient_selection_rules.post_trigger_recipient_selection_rules(
                model_trigger.results[0], model_rec_rules.results[0]
            )
            task_type_id = self.api_work_task_types.get_list_task_types_return_first_id()
            model_task = self.api_work_tasks.post_add_empty_task(task_type_id[0])
            self.api_work_task_assignment_history.post_add_new_task_to_user(model_user_second.userID, model_task.id)
            self.api_work_tasks.patch_update_task_by_id(model_task.id, {"field": "deadline", "value": f"{result}"})
            self.api_work_task_assignment_history.post_add_new_task_to_user_date_end(model_user_second.userID, model_task.id)
            success, message = wait_for_email(
                model_task.number, email_check_start_time, f"Заявка №{model_task.number}", f"Изменено время по заявке {model_task.number}"
                )
            assert success, f"Письмо не прошло проверку или не получено: {message}"
        finally:
            if model_task:
                self.api_work_tasks.delete_task_by_id(model_task.id)    
            if model_trigger:
                self.api_msg_triggers.delete_trigger_by_id(model_trigger.results[0])
            if model_rec_rules:
                self.api_msg_recipient_selection_rules.delete_recipient_selection_rules(model_rec_rules.results[0])
            if model_msg_template:
                self.api_msg_message_templates.delete_message_templates_by_id(model_msg_template.results[0])
            self.api_adm_users.delete_user_by_id(model_user.userID)
            self.api_adm_users.delete_user_by_id(model_user_second.userID)