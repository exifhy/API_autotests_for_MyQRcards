

class Payloads:

    @staticmethod
    def post_add_asset_type_payload(
            name: str,
            host: bool,
            default: bool,
            **kwargs
    ) -> list:
        payload = [
            {
                "name": name,
                "isHostable": host,
                "isDefault": default
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def put_update_asset_type_payload(
            asset_type_id: int,
            name: str,
            host: bool,
            default: bool,
            **kwargs
    ) -> list:
        payload = [
            {
                "id": asset_type_id,
                "name": name,
                "isHostable": host,
                "isDefault": default
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload
