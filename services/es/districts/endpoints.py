import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_districts_endpoint = f'{HOST}/ES/Districts'
    delete_districts_endpoint = f'{HOST}/ES/Districts'
    get_list_districts_available_to_user_endpoint = f'{HOST}/ES/Districts'
    update_districts_endpoint = f'{HOST}/ES/Districts'
    put_update_parent_and_district_sorting_endpoint = f'{HOST}/ES/Districts/parentAndReorder'

    @staticmethod
    def get_info_district_available_to_user_by_id_endpoint(district_id: int) -> str:
        return f'{HOST}/ES/Districts/{district_id}'

    @staticmethod
    def delete_districts_by_id_endpoint(district_id: int) -> str:
        return f'{HOST}/ES/Districts/{district_id}'
