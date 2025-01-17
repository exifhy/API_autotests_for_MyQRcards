import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_actual_inventories_endpoint = f'{HOST}/WH/Inventories/actual'
    get_list_inventories_endpoint = f'{HOST}/WH/Inventories'
    put_update_inventories_endpoint = f'{HOST}/WH/Inventories'
    post_inventories_endpoint = f'{HOST}/WH/Inventories'
    delete_inventories_endpoint = f'{HOST}/WH/Inventories'

    @staticmethod
    def delete_inventories_by_id_endpoint(inventory_id: int) -> str:
        return f'{HOST}/WH/Inventories/{inventory_id}'
