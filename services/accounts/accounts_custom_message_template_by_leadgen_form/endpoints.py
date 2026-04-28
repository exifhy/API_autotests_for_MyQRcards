from config.config import HOST


class Endpoints:
    get_accounts_custom_message_template_by_leadgen_form_endpoint = (
        f"{HOST}/accounts/{{account_id}}/cards/{{card_id}}/LeadGenForms/{{leadgen_form_id}}/MessageTemplate"
    )

