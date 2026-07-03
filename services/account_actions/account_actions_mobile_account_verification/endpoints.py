from config.config import HOST


class Endpoints:
    create_mobile_account_verification_endpoint = f"{HOST}/accountActions/MobileAccountVerification"
    create_mobile_account_verification_silent_endpoint = f"{HOST}/accountActions/MobileAccountVerification/silent"
