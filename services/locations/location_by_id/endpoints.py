from config.config import HOST


class Endpoints:
    get_location_by_id_endpoint = f"{HOST}/Locations/{{location_id}}"

