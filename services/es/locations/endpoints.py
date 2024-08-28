import os


HOST = "https://dev-api.hubex.ru/fsm" if os.environ["ENVIRON"] == 'qa' else "https://api.hubex.ru/fsm"


class Endpoints:

    add_locations_endpoint = f'{HOST}/ES/Locations'

    @staticmethod
    def delete_location_by_id(loc_id: int) -> str:
        return f'{HOST}/ES/Locations/{loc_id}/remove'

    @staticmethod
    def delete_locations() -> str:
        return f'{HOST}/ES/Locations/remove'
