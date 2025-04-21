from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    get_list_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    delete_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    put_update_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    head_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates'
    get_download_qr_code_task_templates_endpoint = f'{HOST}/WORK/TaskTemplates/download'

    @staticmethod
    def get_task_template_by_id_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}'

    @staticmethod
    def get_download_qr_code_task_template_by_id_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/download'

    @staticmethod
    def get_public_task_template_by_id_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/public'

    @staticmethod
    def put_publish_task_template_by_id_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/publish'

    @staticmethod
    def put_unpublish_task_template_by_id_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/unpublish'

    @staticmethod
    def post_assignment_task_templates_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/assignment'

    @staticmethod
    def get_excluded_assets_task_templates_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/excludedAssets'

    @staticmethod
    def delete_excluded_assets_task_templates_by_asset_id_endpoint(task_templates_id: str, asset_id: int) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/excludedAssets/{asset_id}'

    @staticmethod
    def get_list_assignment_task_templates_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/assignment'

    @staticmethod
    def post_task_templates_for_schedules_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules'

    @staticmethod
    def get_task_templates_for_schedules_endpoint(task_templates_id: str) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules'

    @staticmethod
    def post_task_templates_for_schedules_appointments_endpoint(task_templates_id: str, schedule_id: int) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules/{schedule_id}/appointments'

    @staticmethod
    def activate_schedule_endpoint(task_templates_id: str, schedules_id: int) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules/{schedules_id}/activate'

    @staticmethod
    def deactivate_schedule_endpoint(task_templates_id: str, schedules_id: int) -> str:
        return f'{HOST}/WORK/TaskTemplates/{task_templates_id}/schedules/{schedules_id}/deactivate'
