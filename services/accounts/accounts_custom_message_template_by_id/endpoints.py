from config.config import HOST


class Endpoints:
    get_accounts_custom_message_template_by_id_endpoint = (
        f"{HOST}/accounts/{{account_id}}/CustomMessageTemplates/{{template_id}}"
    )
