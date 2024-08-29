

class Payloads:

    @staticmethod
    def add_districts_payload(district_name: str, notes: str, status: bool) -> list:
        payload = [
            {
                "name": district_name,
                "description": notes,
                "isDefault": status
            }
        ]
        return payload

