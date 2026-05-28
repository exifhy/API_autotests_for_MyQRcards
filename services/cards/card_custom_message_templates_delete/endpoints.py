from config.config import HOST


class Endpoints:
    delete_card_custom_message_templates_endpoint = f"{HOST}/Cards/{{card_id}}/customMessageTemplates"

