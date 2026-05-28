from config.config import HOST


class Endpoints:
    get_subscription_contacts_endpoint = f"{HOST}/Subscriptions/{{sub_id}}/contacts"
