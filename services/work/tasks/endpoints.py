import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_task_endpoint = f'{HOST}/WORK/tasks'

    @staticmethod
    def delete_task_by_id_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}'
