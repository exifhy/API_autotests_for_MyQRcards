import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_work_types_endpoint = f'{HOST}/WORK/WorkTypes'
    put_work_types_publish_endpoint = f'{HOST}/WORK/WorkTypes/publish'
    put_work_types_unpublish_endpoint = f'{HOST}/WORK/WorkTypes/unpublish'

    @staticmethod
    def delete_work_types_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}'

    @staticmethod
    def get_data_work_types_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}'

    @staticmethod
    def put_work_types_publish_by_id_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}/publish'

    @staticmethod
    def put_work_types_unpublish_by_id_endpoint(worktype_id: int) -> str:
        return f'{HOST}/WORK/WorkTypes/{worktype_id}/unpublish'

