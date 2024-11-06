import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_queri_endpoint = f'{HOST}/ES/AssetListQueries'
    get_list_queries_available_in_tenant_endpoint = f'{HOST}/ES/AssetListQueries'
    put_update_queri_endpoint = f'{HOST}/ES/AssetListQueries'
    delete_queri_endpoint = f'{HOST}/ES/AssetListQueries'

    @staticmethod
    def get_queri_by_id(queri_id: int) -> str:
        return f'{HOST}/ES/AssetListQueries/{queri_id}'

    @staticmethod
    def delete_queri_by_id(queri_id: int) -> str:
        return f'{HOST}/ES/AssetListQueries/{queri_id}'

    @staticmethod
    def delete_remove_queri() -> str:
        return f'{HOST}/ES/AssetListQueries/remove'

    @staticmethod
    def delete_remove_queri_by_id(queri_id: int) -> str:
        return f'{HOST}/ES/AssetListQueries/{queri_id}/remove'
