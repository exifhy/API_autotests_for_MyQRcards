from config.config import HOST


class Endpoints:
    download_subscription_contacts_csv_endpoint = f"{HOST}/Subscriptions/{{sub_id}}/contacts/download"
