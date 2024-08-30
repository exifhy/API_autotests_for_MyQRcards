import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_location_to_object_endpoint = f'{HOST}/ES/AssetLocations'
    get_list_location_by_object_endpoint = f'{HOST}/ES/AssetLocations'
    update_location_by_object_endpoint = f'{HOST}/ES/AssetLocations'
    unbind_of_location_from_object_endpoint = f'{HOST}/ES/AssetLocations'
