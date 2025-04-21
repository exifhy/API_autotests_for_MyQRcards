from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_warehouses_by_id_endpoint(wh_id: int) -> str:
        return f'{HOST}/WH/Warehouses/{wh_id}'

    @staticmethod
    def delete_warehouses_by_id_endpoint(wh_id: int) -> str:
        return f'{HOST}/WH/Warehouses/{wh_id}'

    get_list_warehouses_endpoint = f'{HOST}/WH/Warehouses'
    put_update_warehouses_endpoint = f'{HOST}/WH/Warehouses'
    post_add_warehouses_endpoint = f'{HOST}/WH/Warehouses'
    delete_warehouses_endpoint = f'{HOST}/WH/Warehouses'
    head_warehouses_endpoint = f'{HOST}/WH/Warehouses'
    get_warehouses_v2_endpoint = f'{HOST}/WH/Warehouses/V2'
    put_restore_warehouses_endpoint = f'{HOST}/WH/Warehouses/restore'

    @staticmethod
    def put_restore_warehouses_by_id_endpoint(wh_id: int) -> str:
        return f'{HOST}/WH/Warehouses/{wh_id}/restore'
