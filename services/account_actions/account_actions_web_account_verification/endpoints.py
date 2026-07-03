from config.config import HOST


class Endpoints:
    create_web_account_verification_endpoint = f"{HOST}/accountActions/WebAccountVerification"
    create_web_account_verification_silent_endpoint = f"{HOST}/accountActions/WebAccountVerification/silent"
