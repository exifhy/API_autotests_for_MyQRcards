from config.config import HOST


class Endpoints:
    create_subscription_invitation_endpoint = f"{HOST}/Subscriptions/{{sub_id}}/invitation"
