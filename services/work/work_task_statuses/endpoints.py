from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_task_statuses_endpoint = f'{HOST}/WORK/TaskStatuses'
    put_update_task_statuses_endpoint = f'{HOST}/WORK/TaskStatuses'
    post_add_task_statuses_endpoint = f'{HOST}/WORK/TaskStatuses'
    delete_task_statuses_by_list_endpoint = f'{HOST}/WORK/TaskStatuses'

    @staticmethod
    def get_task_statuses_by_id_endpoint(task_status_id: int) -> str:
        return f'{HOST}/WORK/TaskStatuses/{task_status_id}'

    @staticmethod
    def delete_task_statuses_by_id_endpoint(task_status_id: int) -> str:
        return f'{HOST}/WORK/TaskStatuses/{task_status_id}'
