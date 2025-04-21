from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_query_endpoint = f'{HOST}/ES/AssetListQueries'
    get_list_queries_available_in_tenant_endpoint = f'{HOST}/ES/AssetListQueries'
    put_update_query_endpoint = f'{HOST}/ES/AssetListQueries'
    delete_queries_endpoint = f'{HOST}/ES/AssetListQueries'
    delete_remove_query_endpoint = f'{HOST}/ES/AssetListQueries/remove'

    @staticmethod
    def get_query_by_id(queri_id: int) -> str:
        return f'{HOST}/ES/AssetListQueries/{queri_id}'

    @staticmethod
    def delete_query_by_id(queri_id: int) -> str:
        return f'{HOST}/ES/AssetListQueries/{queri_id}'

    @staticmethod
    def delete_remove_query_by_id(queri_id: int) -> str:
        return f'{HOST}/ES/AssetListQueries/{queri_id}/remove'
