from config.config import HOST


class Endpoints:
    create_accounts_custom_message_templates_endpoint = f"{HOST}/accounts/{{account_id}}/CustomMessageTemplates"
