import time


class Payloads:
    @staticmethod
    def build_accounts_card_metrics_update_payload(*, metric_type_id: int) -> list[dict]:
        return [
            {
                "MetricID": f"AT_ACCOUNT_METRIC_{int(time.time())}",
                "MetricTypeID": int(metric_type_id),
            }
        ]
