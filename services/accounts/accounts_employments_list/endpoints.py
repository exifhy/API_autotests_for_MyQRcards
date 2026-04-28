from config.config import HOST


class Endpoints:
    get_accounts_employments_endpoint = f"{HOST}/accounts/{{account_id}}/employments"
