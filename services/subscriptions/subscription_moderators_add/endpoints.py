from config.config import HOST


class Endpoints:
    add_subscription_moderators_endpoint = f"{HOST}/subscriptions/{{sub_id}}/moderators"
