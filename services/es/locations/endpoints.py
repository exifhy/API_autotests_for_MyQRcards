import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_locations_endpoint = f'{HOST}/ES/Locations'
    delete_locations_endpoint = f'{HOST}/ES/Locations'
    remove_locations_endpoint = f'{HOST}/ES/Locations/remove'

    @staticmethod
    def delete_location_by_id(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}'

    @staticmethod
    def remove_location_by_id(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}/remove'
