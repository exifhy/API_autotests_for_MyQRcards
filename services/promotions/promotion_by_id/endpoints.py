from config.config import HOST


class Endpoints:
    get_promotion_by_id_endpoint = f"{HOST}/promotions/{{promotion_id}}"

