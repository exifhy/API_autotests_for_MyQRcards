

class Payloads:

    @staticmethod
    def post_add_asset_class_payload(name: str, default: bool, **kwargs) -> list:
        payload = [
            {
                "name": name,
                "isDefault": default
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def put_update_asset_class_payload(
            asset_class_id: int,
            name: str,
            default: bool,
            **kwargs
    ) -> list:
        payload = [
            {
                "id": asset_class_id,
                "name": name,
                "isDefault": default
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload

    @staticmethod
    def delete_asset_class_payload(*args) -> list:
        return [*args]
