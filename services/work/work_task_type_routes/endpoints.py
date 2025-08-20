from config.config import HOST


class Endpoints:

    put_update_task_type_routes_endpoint = f'{HOST}/WORK/TaskTypeRoutes'
    post_task_type_routes_endpoint = f'{HOST}/WORK/TaskTypeRoutes'
    delete_task_type_routes_by_list_endpoint = f'{HOST}/WORK/TaskTypeRoutes'

    @staticmethod
    def delete_task_type_routes_by_id_endpoint(route_id: int) -> str:
        return f'{HOST}/WORK/TaskTypeRoutes/{route_id}'
