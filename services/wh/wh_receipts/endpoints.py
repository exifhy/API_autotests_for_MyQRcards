import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_receipt_by_id_endpoint(receipt_id: int) -> str:
        return f'{HOST}/WH/Receipts/{receipt_id}'

    @staticmethod
    def delete_receipt_by_id_endpoint(receipt_id: int) -> str:
        return f'{HOST}/WH/Receipts/{receipt_id}'

    get_list_receipts_endpoint = f'{HOST}/WH/Receipts'
    put_update_receipts_endpoint = f'{HOST}/WH/Receipts'
    post_add_receipts_endpoint = f'{HOST}/WH/Receipts'
    delete_receipts_endpoint = f'{HOST}/WH/Receipts'
    head_receipts_endpoint = f'{HOST}/WH/Receipts'
    put_restore_receipts_endpoint = f'{HOST}/WH/Receipts/restore'

    @staticmethod
    def put_restore_receipts_by_id_endpoint(receipt_id: int) -> str:
        return f'{HOST}/WH/Receipts/{receipt_id}/restore'

    @staticmethod
    def get_list_items_receipts_by_id_endpoint(receipt_id: int) -> str:
        return f'{HOST}/WH/Receipts/{receipt_id}/items'

    post_items_receipts_endpoint = f'{HOST}/WH/Receipts/items'
    delete_items_receipts_endpoint = f'{HOST}/WH/Receipts/items'

    @staticmethod
    def delete_receipts_by_receipt_id_material_id_endpoint(receipt_id: int, material_id: int) -> str:
        return f'{HOST}/WH/Receipts/{receipt_id}/items/{material_id}'
