from config.config import HOST


class Endpoints:
    get_card_leadgen_form_by_id_endpoint = f"{HOST}/Cards/{{card_id}}/leadGenForms/{{leadgen_form_id}}"

