import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_task_types_endpoint = f'{HOST}/WORK/TaskTypes'
    put_update_task_types_endpoint = f'{HOST}/WORK/TaskTypes'
    post_add_task_types_endpoint = f'{HOST}/WORK/TaskTypes'
    delete_task_types_endpoint = f'{HOST}/WORK/TaskTypes'

    @staticmethod
    def get_task_types_by_id_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}'

    @staticmethod
    def delete_task_types_by_id_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}'

    @staticmethod
    def get_district_for_task_types_by_id_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}/districts'

    @staticmethod
    def get_route_for_task_types_by_id_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}/route'

    @staticmethod
    def get_list_task_types_related_to_work_types_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}/worktypes'

    @staticmethod
    def post_bind_list_work_types_to_task_type_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}/worktypes'

    @staticmethod
    def delete_unbind_work_types_from_task_type_endpoint(task_type_id: int) -> str:
        return f'{HOST}/WORK/TaskTypes/{task_type_id}/worktypes'
