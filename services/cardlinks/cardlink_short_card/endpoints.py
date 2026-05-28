from config.config import get_host


class Endpoints:
    @property
    def get_cardlink_short_card_endpoint(self) -> str:
        return f"{get_host()}/cardLinks/{{card_link}}/short/card"
