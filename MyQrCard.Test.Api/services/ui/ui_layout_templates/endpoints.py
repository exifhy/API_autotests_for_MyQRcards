from config.config import HOST


class Endpoints:

    post_add_default_template_endpoint = f'{HOST}/UI/LayoutTemplates/default'

    @staticmethod
    def put_reset_template_to_default_condition_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}/reset'

    get_list_layout_templates_endpoint = f'{HOST}/UI/LayoutTemplates'

    post_create_template_endpoint = f'{HOST}/UI/LayoutTemplates'

    @staticmethod
    def get_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}'

    @staticmethod
    def put_update_template_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}'

    @staticmethod
    def delete_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}'

    @staticmethod
    def get_templates_by_type_endpoint(task_type_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/bytype/{task_type_id}'

    @staticmethod
    def get_task_types_layout_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}/taskTypes'

    @staticmethod
    def put_set_task_types_to_layout_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}/taskTypes'

    @staticmethod
    def delete_task_types_from_layout_template_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}/taskTypes'

    @staticmethod
    def get_components_layout_templates_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}/Components'

    @staticmethod
    def get_attributes_layout_templates_endpoint(template_id: int) -> str:
        return f'{HOST}/UI/LayoutTemplates/{template_id}/Attributes'
