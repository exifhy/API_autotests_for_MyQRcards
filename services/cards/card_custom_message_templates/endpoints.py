from config.config import HOST


class Endpoints:
    get_card_custom_message_templates_endpoint = f"{HOST}/Cards/{{card_id}}/customMessageTemplates"
