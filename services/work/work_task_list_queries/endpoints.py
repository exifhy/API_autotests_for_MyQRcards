import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:
    get_task_list_queries_endpoint = f'{HOST}/WORK/TaskListQueries'
    put_task_list_queries_endpoint = f'{HOST}/WORK/TaskListQueries'
    post_task_list_queries_endpoint = f'{HOST}/WORK/TaskListQueries'
    delete_task_list_queries_endpoint = f'{HOST}/WORK/TaskListQueries'

    @staticmethod
    def get_task_list_queries_by_id_endpoint(query_id: int) -> str:
        return f'{HOST}/WORK/TaskListQueries/{query_id}'

    @staticmethod
    def delete_task_list_queries_by_id_endpoint(query_id: int) -> str:
        return f'{HOST}/WORK/TaskListQueries/{query_id}'

    delete_remove_task_list_queries_endpoint = f'{HOST}/WORK/TaskListQueries/remove'

    @staticmethod
    def delete_remove_task_list_queries_by_id_endpoint(query_id: int) -> str:
        return f'{HOST}/WORK/TaskListQueries/{query_id}/remove'
