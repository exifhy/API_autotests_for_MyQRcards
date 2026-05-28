from config.config import HOST


class Endpoints:
    merge_subscription_designsettings_endpoint = f"{HOST}/subscriptions/{{sub_id}}/designsettings"
