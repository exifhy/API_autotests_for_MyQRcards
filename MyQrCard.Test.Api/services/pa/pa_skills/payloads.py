

class Payloads:

    @staticmethod
    def post_add_skills_for_tenant_payload(*skills: tuple[str, str, bool]) -> list:
        payload = [
            {"name": name, "description": notes, "isOptional": status}
            for name, notes, status in skills
        ]
        return payload

    @staticmethod
    def delete_skills_by_list_payload(*args) -> list:
        return [*args]

    @staticmethod
    def put_update_skills_for_tenant_payload(*skills: tuple[int, str, str, bool]) -> list:
        payload = [
            {"id": skill_id, "name": name, "description": notes, "isOptional": status}
            for skill_id, name, notes, status in skills
        ]
        return payload
