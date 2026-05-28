from datetime import datetime, timedelta


class Payloads:
    @staticmethod
    def build_exports_statistic_params(*, now: datetime | None = None, days_back: int = 2) -> dict:
        now = now or datetime.now()
        date_from = (now - timedelta(days=days_back)).replace(hour=0, minute=0, second=0, microsecond=0)
        date_till = now.replace(hour=23, minute=59, second=59, microsecond=0)
        return {
            "DateFrom": date_from.strftime("%Y-%m-%dT%H:%M:%S"),
            "DateTill": date_till.strftime("%Y-%m-%dT%H:%M:%S"),
        }
