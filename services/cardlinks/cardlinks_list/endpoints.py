from config.config import get_host


class Endpoints:
    @property
    def get_cardlinks_endpoint(self) -> str:
        return f"{get_host()}/cardLinks"
