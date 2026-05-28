from config.config import HOST


class Endpoints:
    post_register_endpoint = f"{HOST}/AUTH/Accounts/register"
    get_accounts_endpoint = f"{HOST}/AUTH/Accounts"
