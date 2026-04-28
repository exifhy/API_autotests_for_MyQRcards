from config.config import HOST


class Endpoints:
    delete_subscription_invitation_endpoint = f"{HOST}/Subscriptions/{{sub_id}}/invitation/{{invite_id}}"
