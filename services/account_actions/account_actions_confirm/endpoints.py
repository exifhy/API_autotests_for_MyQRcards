from config.config import HOST


class Endpoints:
    confirm_account_action_endpoint = f"{HOST}/accountActions/{{guid}}"
