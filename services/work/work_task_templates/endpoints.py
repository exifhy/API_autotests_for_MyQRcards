import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    get_list_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    marks_task_templates_as_removed_endpoint = f'{HOST}/WORK/TaskTemplates'

    @staticmethod
    def assignment_task_templates_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/assignment'

    @staticmethod
    def task_templates_for_schedules_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules'

    @staticmethod
    def activate_schedule_endpoint(task_templates_id: str, schedules_id: int) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules/{schedules_id}/activate'

    @staticmethod
    def deactivate_schedule_endpoint(task_templates_id: str, schedules_id: int) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules/{schedules_id}/deactivate'
