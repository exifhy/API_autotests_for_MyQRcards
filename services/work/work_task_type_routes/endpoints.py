import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    put_update_task_type_routes_endpoint = f'{HOST}/WORK/TaskTypeRoutes'
    post_task_type_routes_endpoint = f'{HOST}/WORK/TaskTypeRoutes'
    delete_task_type_routes_by_list_endpoint = f'{HOST}/WORK/TaskTypeRoutes'

    @staticmethod
    def delete_task_type_routes_by_id_endpoint(route_id: int) -> str:
        return f'{HOST}/WORK/TaskTypeRoutes/{route_id}'
