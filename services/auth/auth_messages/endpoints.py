import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_message_verify_email_endpoint = f'{HOST}/AUTH/Messages/verifyEmail'
    post_message_verify_phone_endpoint = f'{HOST}/AUTH/Messages/verifyPhone'
    post_message_request_password_change_endpoint = f'{HOST}/AUTH/Messages/requestPasswordChange'
    