from config.config import HOST


class Endpoints:
    get_card_metrics_endpoint = f"{HOST}/Cards/{{card_id}}/metrics"

