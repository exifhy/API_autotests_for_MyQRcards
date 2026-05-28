from config.config import get_host


class Endpoints:
    @property
    def cardlink_statistic_download_endpoint(self) -> str:
        return f"{get_host()}/cardlinks/{{card_link}}/statisticdownload"
