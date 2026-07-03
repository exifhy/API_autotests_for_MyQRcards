

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
    def put_update_district_payload(district_id: int, district_name: str, notes: str, status: bool) -> list:
        payload = [
            {
                "id": district_id,
                "name": district_name,
                "description": notes,
                "isDefault": status
            }
        ]
        return payload

    @staticmethod
    def put_update_parent_district_payload(district_id: int, parent_id: int) -> list:
        payload = [
            {
                "id": district_id,
                "parentID": parent_id
            }
        ]
        return payload

    @staticmethod
    def put_update_district_sorting_payload(district_id: int, sorted_id: int) -> list:
        payload = [
            {
                "id": district_id,
                "sortOrder": sorted_id
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