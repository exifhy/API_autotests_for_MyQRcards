from config.config import HOST


class Endpoints:
    update_card_designsettings_endpoint = f"{HOST}/Cards/{{card_id}}/designsettings"

