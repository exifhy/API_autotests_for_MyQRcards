from config.config import HOST

class Endpoints:

    @staticmethod
    def get_message_template_endpoint(template_id: int) -> str:
        return f'{HOST}/MSG/MessageTemplates/{template_id}'

    @staticmethod
    def delete_message_template_endpoint(template_id: int) -> str:
        return f'{HOST}/MSG/MessageTemplates/{template_id}'

    @staticmethod
    def put_validate_message_template_endpoint(template_id: int) -> str:
        return f'{HOST}/MSG/MessageTemplates/{template_id}/validate'

    get_message_templates_list_endpoint = f'{HOST}/MSG/MessageTemplates'
    post_message_templates_endpoint = f'{HOST}/MSG/MessageTemplates'
    put_update_message_templates_endpoint = f'{HOST}/MSG/MessageTemplates'
    delete_message_templates_endpoint = f'{HOST}/MSG/MessageTemplates'
