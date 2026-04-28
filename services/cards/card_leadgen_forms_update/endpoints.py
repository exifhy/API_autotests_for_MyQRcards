from config.config import HOST


class Endpoints:
    update_card_leadgen_forms_endpoint = f"{HOST}/Cards/{{card_id}}/leadGenForms"

