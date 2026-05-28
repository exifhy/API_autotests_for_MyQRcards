from config.config import HOST


class Endpoints:
    update_accounts_custom_message_templates_endpoint = f"{HOST}/accounts/{{account_id}}/CustomMessageTemplates"
