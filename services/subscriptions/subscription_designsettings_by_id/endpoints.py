from config.config import HOST


class Endpoints:
    get_subscription_designsettings_endpoint = f"{HOST}/Subscriptions/{{sub_id}}/designsettings"
