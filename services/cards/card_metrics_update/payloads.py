import time


class Payloads:
    @staticmethod
    def build_card_metrics_update_payload(*, metric_type_id: int) -> list[dict]:
        return [
            {
                "metricID": f"AT_METRIC_{int(time.time())}",
                "metricTypeID": int(metric_type_id),
                "isActive": True,
            }
        ]
