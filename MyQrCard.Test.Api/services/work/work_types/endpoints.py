from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_list_check_lists_work_type_endpoint(work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/checkLists'

    @staticmethod
    def post_add_check_lists_to_work_type_endpoint(work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/checkLists'

    @staticmethod
    def delete_check_lists_from_work_type_endpoint(work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/checkLists'

    @staticmethod
    def post_add_check_lists_to_work_type_by_id_endpoint(work_type_id: int, check_list_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/checkLists/{check_list_id}'

    @staticmethod
    def delete_check_lists_from_work_type_by_id_endpoint(work_type_id: int, check_list_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/checkLists/{check_list_id}'

    add_work_types_endpoint = f'{HOST}/WORK/WorkTypes'
    get_list_work_types_endpoint = f'{HOST}/WORK/WorkTypes'
    put_update_work_types_endpoint = f'{HOST}/WORK/WorkTypes'
    delete_work_types_by_list_endpoint = f'{HOST}/WORK/WorkTypes'
    put_work_types_publish_endpoint = f'{HOST}/WORK/WorkTypes/publish'
    put_work_types_unpublish_endpoint = f'{HOST}/WORK/WorkTypes/unpublish'

    @staticmethod
    def delete_work_types_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}'

    @staticmethod
    def get_data_work_types_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}'

    @staticmethod
    def get_work_types_parent_work_type_id_endpoint(parent_work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{parent_work_type_id}/workTypes'

    @staticmethod
    def get_work_types_parent_work_type_id_all_endpoint(parent_work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{parent_work_type_id}/workTypes/all'

    @staticmethod
    def put_work_types_publish_by_id_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}/publish'

    @staticmethod
    def put_work_types_unpublish_by_id_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}/unpublish'

    @staticmethod
    def get_work_types_task_types_endpoint(work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/taskTypes'

    @staticmethod
    def post_add_task_types_to_work_types_endpoint(work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/taskTypes'

    @staticmethod
    def delete_task_types_from_work_types_endpoint(work_type_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{work_type_id}/taskTypes'

