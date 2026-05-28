from config.config import HOST


class Endpoints:
    get_account_endpoint = f"{HOST}/accounts/{{account_id}}"
