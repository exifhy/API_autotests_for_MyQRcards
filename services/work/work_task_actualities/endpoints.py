import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_task_actualities_endpoint = f'{HOST}/WORK/taskActualities'
    put_update_task_actualities_endpoint = f'{HOST}/WORK/taskActualities'
    post_add_task_actualities_endpoint = f'{HOST}/WORK/taskActualities'
    delete_task_actualities_endpoint = f'{HOST}/WORK/taskActualities'

    @staticmethod
    def get_task_actualities_by_id(act_task_id: int) -> str:
        return f'{HOST}/WORK/taskActualities/{act_task_id}'

    @staticmethod
    def delete_task_actualities_by_id(act_task_id: int) -> str:
        return f'{HOST}/WORK/taskActualities/{act_task_id}'
