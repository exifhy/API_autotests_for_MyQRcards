from config.config import HOST


class Endpoints:
    get_proxy_card_cardlink_endpoint = f"{HOST}/proxy/card/cardlink/{{token}}"
