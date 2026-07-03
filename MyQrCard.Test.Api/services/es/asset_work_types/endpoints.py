from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_asset_work_type_endpoint = f'{HOST}/ES/assetWorkTypes'
    delete_work_type_from_asset_endpoint = f'{HOST}/ES/assetWorkTypes'
