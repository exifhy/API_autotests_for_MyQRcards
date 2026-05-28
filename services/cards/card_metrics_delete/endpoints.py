from config.config import HOST


class Endpoints:
    delete_card_metrics_endpoint = f"{HOST}/Cards/{{card_id}}/metrics"

