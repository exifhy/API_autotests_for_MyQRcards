from config.config import HOST


class Endpoints:

    post_add_user_asset_list_queries_endpoint = f'{HOST}/ADM/UserAssetListQueries'
    delete_user_asset_list_queries_endpoint = f'{HOST}/ADM/UserAssetListQueries'

    @staticmethod
    def post_add_user_asset_list_queries_by_list_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/UserAssetListQueries/{user_id}'

    @staticmethod
    def delete_user_asset_list_queries_by_list_endpoint(user_id: int) -> str:
        return f'{HOST}/ADM/UserAssetListQueries/{user_id}'
