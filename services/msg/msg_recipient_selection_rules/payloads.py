from faker import Faker

fake_ru = Faker('ru_RU')

class Payloads:

    @staticmethod
    def put_update_recipient_selection_rules_payload(
        recipient_id: int,
        custom_role_id: int
    ) -> list:
        payload = [
            {
                "id": recipient_id,
                "description": "Начальник сервисной службы",
                "customRoleID": custom_role_id,
                "useUnverifiedContacts": True
            }
        ]
        return payload

    @staticmethod
    def post_recipient_selection_rules_payload(
        custom_role_id: int
    ) -> list:
        payload = [
            {
                "description": fake_ru.bban(),
                "customRoleID": str(custom_role_id),
                "useUnverifiedContacts": True
            }
        ]
        return payload