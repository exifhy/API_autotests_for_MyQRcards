from config.config import get_host


class Endpoints:
    @property
    def get_cardlink_download_endpoint(self) -> str:
        return f"{get_host()}/cardLinks/{{card_link}}/card/download"
