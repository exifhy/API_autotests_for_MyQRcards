import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_districts_endpoint = f'{HOST}/ES/Districts'
    marks_districts_as_remote_endpoint = f'{HOST}/ES/Districts'
    get_list_districts_available_to_user_endpoint = f'{HOST}/ES/Districts'
    update_districts_endpoint = f'{HOST}/ES/Districts'

    @staticmethod
    def get_info_district_available_to_user_by_id_endpoint(district_id: int) -> str:
        return f'{HOST}/ES/Districts/{district_id}'

    @staticmethod
    def marks_districts_as_remote_by_id_endpoint(district_id: int) -> str:
        return f'{HOST}/ES/Districts/{district_id}'
