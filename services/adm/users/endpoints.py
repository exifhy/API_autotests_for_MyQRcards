import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_users_endpoint = f'{HOST}/ADM/Users'
    get_list_users_endpoint = f'{HOST}/ADM/Users'
    post_add_api_user_in_tenant_endpoint = f'{HOST}/ADM/Users/api'
    get_list_asset_queries_to_current_user_endpoint = f'{HOST}/ADM/users/this/AssetListQueries/'

    @staticmethod
    def delete_user_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}'

    @staticmethod
    def get_user_info_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}'

    @staticmethod
    def put_update_user_info_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}'

    @staticmethod
    def get_users_roles_by_id_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/Users/{user_id}/roles'

