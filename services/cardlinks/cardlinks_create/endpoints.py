from config.config import get_host


class Endpoints:
    @property
    def create_cardlinks_endpoint(self) -> str:
        return f"{get_host()}/cards/{{card_id}}/links"
