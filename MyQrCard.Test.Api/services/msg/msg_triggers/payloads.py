from faker import Faker

fake_ru = Faker('ru_RU')

class Payloads:
    
    @staticmethod
    def put_update_triggers_payload(
        trigger_id: int,
        description: str,
        event_id: int,
        template_id: int
    ) -> list:
        payload = [
            {
                "id": trigger_id,
                "description": description,
                "isNotifyDuringWorkHours": True,
                "isNotifyDuringDutyHours": True,
                "isNotifyDuringOtherHours": True,
                "eventID": event_id,
                "messageTemplateID": template_id
            }
        ]
        return payload

    @staticmethod
    def post_triggers_payload(
        event_id: int,
        template_id: int
    ) -> list:
        payload = [
            {
                "description": f"Триггер-{fake_ru.bban()}",
                "isNotifyDuringWorkHours": True,
                "isNotifyDuringDutyHours": True,
                "isNotifyDuringOtherHours": True,
                "eventID": event_id,
                "messageTemplateID": template_id
            }
        ]
        return payload