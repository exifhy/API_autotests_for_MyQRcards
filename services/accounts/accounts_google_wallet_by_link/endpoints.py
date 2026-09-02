from config.config import HOST


class Endpoints:
    create_google_wallet_by_link_endpoint = f"{HOST}/Accounts/GoogleWallet/{{card_link}}/card"
