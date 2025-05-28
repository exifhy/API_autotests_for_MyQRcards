from config.config import HOST


class Endpoints:

    account_authentication_by_basic_authorization_endpoint = f'{HOST}/AUTHN/accounts/login'
    account_authentication_by_sso_endpoint = f'{HOST}/AUTHN/accounts/login/sso'
    generating_code_for_authorization_by_sms_endpoint = f'{HOST}/AUTHN/accounts/smssend'
    check_sms_code_endpoint = f'{HOST}/AUTHN/accounts/smslogin'
