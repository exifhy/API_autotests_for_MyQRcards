import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    account_authentication_by_basic_authorization_endpoint = f'{HOST}/AUTHN/accounts/login'
    account_authentication_by_sso_endpoint = f'{HOST}/AUTHN/accounts/login/sso'
    generating_code_for_authorization_by_sms_endpoint = f'{HOST}/AUTHN/accounts/smssend'
    check_sms_code_endpoint = f'{HOST}/AUTHN/accounts/smslogin'
