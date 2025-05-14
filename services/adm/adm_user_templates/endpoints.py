from config.config import HOST


class Endpoints:

    get_list_user_templates_endpoint = f'{HOST}/ADM/UserTemplates'
    post_user_templates_endpoint = f'{HOST}/ADM/UserTemplates'
    put_user_templates_endpoint = f'{HOST}/ADM/UserTemplates'
    delete_user_templates_endpoint = f'{HOST}/ADM/UserTemplates'

    @staticmethod
    def get_user_template_endpoint(template_id: int) -> str:
        return f'{HOST}/ADM/UserTemplates/{template_id}'

    @staticmethod
    def delete_user_template_endpoint(template_id: int) -> str:
        return f'{HOST}/ADM/UserTemplates/{template_id}'

    @staticmethod
    def get_user_templates_districts(template_id: int) -> str:
        return f'{HOST}/ADM/UserTemplates/{template_id}/districts'

    @staticmethod
    def get_user_templates_roles(template_id: int) -> str:
        return f'{HOST}/ADM/UserTemplates/{template_id}/roles'
