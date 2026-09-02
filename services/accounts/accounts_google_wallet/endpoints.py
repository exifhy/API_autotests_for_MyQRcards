from config.config import HOST


class Endpoints:
    create_google_wallet_endpoint = f"{HOST}/Accounts/GoogleWallet/{{card_id}}"
