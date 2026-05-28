from config.config import HOST


class Endpoints:
    get_location_cardlinks_list_endpoint = f"{HOST}/cards/attributes/locations/cardlink/{{card_link_id}}"
