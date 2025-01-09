import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_locations_endpoint = f'{HOST}/ES/Locations'
    put_update_location_endpoint = f'{HOST}/ES/Locations'
    add_locations_endpoint = f'{HOST}/ES/Locations'
    delete_locations_endpoint = f'{HOST}/ES/Locations'
    head_return_quantity_locations = f'{HOST}/ES/Locations'
    remove_locations_endpoint = f'{HOST}/ES/Locations/remove'

    @staticmethod
    def get_location_by_id_endpoint(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}'

    @staticmethod
    def delete_location_by_id(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}'

    @staticmethod
    def remove_location_by_id_endpoint(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}/remove'
