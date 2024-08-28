import os


HOST = "https://dev-api.hubex.ru/fsm" if os.environ["ENVIRON"] == 'qa' else "https://api.hubex.ru/fsm"


class Endpoints:

    add_location_to_object_endpoint = f'{HOST}/ES/AssetLocations'
    get_list_location_by_object_endpoint = f'{HOST}/ES/AssetLocations'
    update_location_by_object_endpoint = f'{HOST}/ES/AssetLocations'
    deleting_location_binding_to_object_endpoint = f'{HOST}/ES/AssetLocations'
