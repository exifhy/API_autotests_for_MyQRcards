from config.config import HOST


class Endpoints:
    create_card_leadgen_form_endpoint = f"{HOST}/Cards/{{card_id}}/leadGenForms"

