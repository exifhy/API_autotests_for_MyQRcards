from config.config import HOST


class Endpoints:
    update_accounts_card_metrics_endpoint = f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/metrics"
