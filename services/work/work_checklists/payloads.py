

class Payloads:

    @staticmethod
    def post_add_checklists_payload(name: str, desc: str) -> list:
        payload = [
            {
                "name": name,
                "description": desc
            }
        ]
        return payload

    @staticmethod
    def delete_checklists_payloads(*args) -> list:
        return [*args]
