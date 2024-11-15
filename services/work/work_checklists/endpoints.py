import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_active_checklists_endpoint = f'{HOST}/WORK/CheckLists'
    put_update_checklists_endpoint = f'{HOST}/WORK/CheckLists'
    post_add_checklists_endpoint = f'{HOST}/WORK/CheckLists'
    delete_checklists_endpoint = f'{HOST}/WORK/CheckLists'

    @staticmethod
    def get_checklist_by_id_endpoint(checklist_id: int) -> str:
        return f'{HOST}/WORK/CheckLists/{checklist_id}'

    @staticmethod
    def delete_checklist_by_id_endpoint(checklist_id: int) -> str:
        return f'{HOST}/WORK/CheckLists/{checklist_id}'

    @staticmethod
    def post_checklist_identifiers_in_tables_of_asset_and_work_types_endpoint(checklist_id: int) -> str:
        return f'{HOST}/WORK/CheckLists/{checklist_id}/assign'

    @staticmethod
    def delete_checklist_identifiers_from_tables_of_asset_and_work_types_endpoint(checklist_id: int) -> str:
        return f'{HOST}/WORK/CheckLists/{checklist_id}/assign'

    @staticmethod
    def get_items_checklist_endpoint(checklist_id: int) -> str:
        return f'{HOST}/WORK/CheckLists/{checklist_id}/items'
