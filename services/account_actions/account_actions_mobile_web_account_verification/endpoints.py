from config.config import HOST


class Endpoints:
    create_mobile_web_account_verification_endpoint = f"{HOST}/accountActions/MobileWebAccountVerification"
    create_mobile_web_account_verification_silent_endpoint = (
        f"{HOST}/accountActions/MobileWebAccountVerification/silent"
    )
