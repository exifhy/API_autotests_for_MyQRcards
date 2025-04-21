from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_asset_classes_endpoint = f'{HOST}/ES/AssetClasses'
    put_update_asset_class_endpoint = f'{HOST}/ES/AssetClasses'
    post_add_asset_class_endpoint = f'{HOST}/ES/AssetClasses'
    delete_asset_class_endpoint = f'{HOST}/ES/AssetClasses'

    @staticmethod
    def get_asset_class_by_id_endpoint(asset_class_id: int) -> str:
        return f'{HOST}/ES/AssetClasses/{asset_class_id}'

    @staticmethod
    def delete_asset_class_by_id_endpoint(asset_class_id: int) -> str:
        return f'{HOST}/ES/AssetClasses/{asset_class_id}'
