

class Payloads:

    @staticmethod
    def put_update_asset_scheme_payload(scheme_id: int, name: str) -> dict:
        payload = {
            "schemaID": scheme_id,
            "name": name
        }
        return payload

    @staticmethod
    def post_create_asset_scheme_payload(
            asset_asset_id: int,
            asset_x: int,
            asset_y: int,
            schema_id: int,
            asset_id: int,
            image_id: int,
            name: str
    ) -> dict:
        payload = {
            "assets": [
                {
                    "assetID": asset_asset_id,
                    "x": asset_x,
                    "y": asset_y
                }
            ],
            "schemaID": schema_id,
            "assetID": asset_id,
            "imageID": image_id,
            "name": name
        }
        return payload

    @staticmethod
    def post_create_asset_scheme_only_name_payload(name: str) -> dict:
        return {"name": name}

    @staticmethod
    def post_bind_asset_scheme_to_asset_payloads(*args) -> list:
        return [*args]

    @staticmethod
    def put_unbind_asset_scheme_to_asset_payloads(*args) -> list:
        return [*args]

    @staticmethod
    def image_size_payload(w: int, h: int) -> dict:
        payload = {
            "width": w,
            "height": h
        }
        return payload

    @staticmethod
    def post_add_points_to_asset_schema_payload(*args) -> list:
        return [*args]

    @staticmethod
    def delete_points_from_asset_schema_payload(*args) -> list:
        return [*args]
