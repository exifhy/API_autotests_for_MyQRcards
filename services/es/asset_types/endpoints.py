from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_asset_types_endpoint = f'{HOST}/ES/AssetTypes'
    put_update_asset_type_endpoint = f'{HOST}/ES/AssetTypes'
    post_add_asset_type_endpoint = f'{HOST}/ES/AssetTypes'
    delete_asset_types_endpoint = f'{HOST}/ES/AssetTypes'

    @staticmethod
    def get_asset_type_by_id_endpoint(asset_type_id: int):
        return f'{HOST}/ES/AssetTypes/{asset_type_id}'

    @staticmethod
    def delete_asset_type_by_id_endpoint(asset_type_id: int):
        return f'{HOST}/ES/AssetTypes/{asset_type_id}'
