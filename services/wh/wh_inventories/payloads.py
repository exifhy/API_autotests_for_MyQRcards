

class Payloads:

    @staticmethod
    def post_add_inventories_payload(date: str, material_data: dict) -> list:
        payload = [
            {
                "inventoryDateFrom": date,
                "materials": [
                    material_data
                ]
            }
        ]
        return payload
