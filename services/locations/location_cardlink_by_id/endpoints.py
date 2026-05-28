from config.config import HOST


class Endpoints:
    get_location_cardlink_by_id_endpoint = f"{HOST}/cards/attributes/locations/{{location_id}}/cardlink/{{card_link_id}}"
