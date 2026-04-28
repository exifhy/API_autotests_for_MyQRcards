from config.config import HOST


class Endpoints:
    get_card_link_leadgen_forms_endpoint = f"{HOST}/Cards/{{card_link_id}}/cardLink/leadGenForms"

