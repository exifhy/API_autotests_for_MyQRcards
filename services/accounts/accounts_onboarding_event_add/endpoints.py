from config.config import HOST


class Endpoints:
    add_account_onboarding_event_endpoint = f"{HOST}/Accounts/onboardingEvents/{{type_id}}"
