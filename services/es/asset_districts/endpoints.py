from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_district_to_object_endpoint = f'{HOST}/ES/assetDistricts'
    delete_districts_from_object_endpoint = f'{HOST}/ES/assetDistricts'


