from config.config import get_host


class Endpoints:
    @property
    def get_cardlink_by_id_endpoint(self) -> str:
        return f"{get_host()}/cardlinks/{{card_link}}"
