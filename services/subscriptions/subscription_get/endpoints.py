from config.config import HOST


class Endpoints:
    get_subscription_endpoint = f"{HOST}/Subscriptions/{{sub_id}}/account/{{account_id}}"
