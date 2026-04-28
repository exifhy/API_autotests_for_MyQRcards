from config.config import HOST


class Endpoints:
    update_subscription_contacts_endpoint = f"{HOST}/subscriptions/{{sub_id}}/contacts"
