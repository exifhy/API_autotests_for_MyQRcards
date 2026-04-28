from config.config import HOST


class Endpoints:
    get_card_leadgen_forms_endpoint = f"{HOST}/Cards/{{card_id}}/leadGenForms"

