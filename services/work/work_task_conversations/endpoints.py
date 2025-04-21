from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_task_conversations_endpoint = f'{HOST}/WORK/taskConversations'
    delete_task_conversations_endpoint = f'{HOST}/WORK/taskConversations'
    head_task_conversations_endpoint = f'{HOST}/WORK/taskConversations'
    delete_remove_task_conversations_endpoint = f'{HOST}/WORK/taskConversations/remove'
