from config.config import HOST


class Endpoints:
    get_account_token_endpoint = f"{HOST}/accounttokens/{{token}}"
