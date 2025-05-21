from config.config import HOST


class Endpoints:

    get_list_permissions_ui_endpoint = f'{HOST}/ADM/PermissionsUi'
    post_add_permissions_ui_endpoint = f'{HOST}/ADM/PermissionsUi'
    delete_permissions_ui_by_list_endpoint = f'{HOST}/ADM/PermissionsUi'
    put_update_permissions_ui_endpoint = f'{HOST}/ADM/PermissionsUi'

    @staticmethod
    def get_permission_ui_by_id_endpoint(permission_id: int) -> str:
        return f'{HOST}/ADM/PermissionsUi/{permission_id}'

    @staticmethod
    def delete_permission_ui_by_id(permission_id: int) -> str:
        return f'{HOST}/ADM/PermissionsUi/{permission_id}'

