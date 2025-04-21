from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    @staticmethod
    def get_list_roles_applications_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}/applications'

    @staticmethod
    def get_list_roles_attachments_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}/attachments'

    @staticmethod
    def get_role_by_id_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}'

    @staticmethod
    def delete_role_by_id_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}'

    get_list_roles_endpoint = f'{HOST}/ADM/Roles'
    put_update_role_endpoint = f'{HOST}/ADM/Roles'
    delete_roles_by_list_endpoint = f'{HOST}/ADM/Roles'
    post_roles_copy_endpoint = f'{HOST}/ADM/Roles/copy'

    @staticmethod
    def get_list_roles_permissions_api_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}/permissionsApi'

    @staticmethod
    def get_list_roles_permissions_ext_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}/permissionsExt'

    @staticmethod
    def get_list_roles_permissions_ui_endpoint(role_id: int) -> str:
        return f'{HOST}/ADM/Roles/{role_id}/permissionsUi'
