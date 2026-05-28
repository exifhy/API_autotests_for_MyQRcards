from config.config import get_host


class Endpoints:
    @property
    def unassign_cardlink_endpoint(self) -> str:
        return f"{get_host()}/cardlinks/{{card_link}}/unassign"
