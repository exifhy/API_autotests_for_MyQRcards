from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_tags_to_asset_endpoint = f'{HOST}/ES/AssetTags'
    delete_tags_from_asset_endpoint = f'{HOST}/ES/AssetTags'
