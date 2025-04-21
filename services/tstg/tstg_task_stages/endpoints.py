from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_task_stages_in_tenant_endpoint = f'{HOST}/TSTG/taskStages'
    put_update_task_stages_endpoint = f'{HOST}/TSTG/taskStages'
    post_add_task_stages_endpoint = f'{HOST}/TSTG/taskStages'
    delete_task_stages_endpoint = f'{HOST}/TSTG/taskStages'
    head_task_stages_endpoint = f'{HOST}/TSTG/taskStages'
    post_task_stages_copy_endpoint = f'{HOST}/TSTG/taskStages/copy'

    @staticmethod
    def get_task_stage_by_id(task_stage_id) -> str:
        return f'{HOST}/TSTG/taskStages/{task_stage_id}'

    @staticmethod
    def delete_task_stage_by_id(task_stage_id) -> str:
        return f'{HOST}/TSTG/taskStages/{task_stage_id}'

    @staticmethod
    def get_task_stage_triggers_by_id(task_stage_id) -> str:
        return f'{HOST}/TSTG/taskStages/{task_stage_id}/messageTriggers'

    @staticmethod
    def post_add_triggers_task_stage_by_id(task_stage_id) -> str:
        return f'{HOST}/TSTG/taskStages/{task_stage_id}/assign'

    @staticmethod
    def get_requirements_task_stage_by_id(task_stage_id) -> str:
        return f'{HOST}/TSTG/taskStages/{task_stage_id}/requirements'
