

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

    @staticmethod
    def add_districts_args_payload(*districts: tuple[str, str, bool]) -> list:
        payload = [
            {"name": name, "description": notes, "isDefault": status}
            for name, notes, status in districts
        ]
        return payload

    @staticmethod
    def delete_districts_by_list_payload(*districts_id: int) -> list:
        return [*districts_id]