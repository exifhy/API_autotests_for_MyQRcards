import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_template_quick_response_endpoint = f'{HOST}/WORK//TemplateQuickResponse'
    put_template_quick_response_endpoint = f'{HOST}/WORK//TemplateQuickResponse'
    post_template_quick_response_endpoint = f'{HOST}/WORK//TemplateQuickResponse'
    delete_template_quick_response_endpoint = f'{HOST}/WORK//TemplateQuickResponse'
    put_update_task_type_template_quick_response_endpoint = f'{HOST}/WORK//TemplateQuickResponse/taskTypes'

    @staticmethod
    def get_template_quick_response_by_id_endpoint(response_id: int) -> str:
        return f'{HOST}/WORK//TemplateQuickResponse/{response_id}'
