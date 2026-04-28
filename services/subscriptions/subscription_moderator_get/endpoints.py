from config.config import HOST


class Endpoints:
    get_subscription_moderator_endpoint = f"{HOST}/subscriptions/{{sub_id}}/moderators/{{account_id}}"
