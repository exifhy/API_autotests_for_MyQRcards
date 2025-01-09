import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    put_task_conversation_deliveries_endpoint = f'{HOST}/WORK/taskConversationDeliveries/read'
