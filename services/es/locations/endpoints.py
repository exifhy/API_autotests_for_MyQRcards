import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_locations_endpoint = f'{HOST}/ES/Locations'

    @staticmethod
    def delete_location_by_id(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}/remove'

    @staticmethod
    def delete_locations() -> str:
        return f'{HOST}/ES/Locations/remove'
