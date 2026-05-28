from config.config import HOST


class Endpoints:
    delete_account_token_endpoint = f"{HOST}/accounttokens/{{token}}"
