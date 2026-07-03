from faker import Faker

fake_ru = Faker('ru_RU')

class Payloads:

    @staticmethod
    def put_update_message_templates_create_task_payload(
        msg_template_id: int,
        provider_id: int
    ) -> list:
        payload = [
            {
                "id": msg_template_id,
                "description": "Новая заявка",
                "subject": "Заявка №{{ TaskNumber }}",
                "content": "Новая заявка {{ TaskNumber }}, по объекту {{ AssetFullName }}",
                "contentTypeID": 2,
                "providerID": provider_id
            }
        ]
        return payload

    @staticmethod
    def put_update_message_template_payload(
        msg_template_id: int,
        description_template: str,
        subject_template: str,
        content_template: str,
        provider_id: int
    ) -> list:
        payload = [
            {
                "id": msg_template_id,
                "description": description_template,
                "subject": subject_template,
                "content": content_template,
                "contentTypeID": 2,
                "providerID": provider_id
            }
        ]
        return payload

    @staticmethod
    def post_message_templates_create_task_email_payload() -> list:
        payload = [
            {
                "description": f"Новая заявка-{fake_ru.bban()}",
                "subject": "Заявка №{{ TaskNumber }}",
                "content": "Новая заявка {{ TaskNumber }}, по объекту {{ AssetFullName }}",
                "contentTypeID": 2,
                "providerID": 1
            }
        ]
        return payload

    @staticmethod
    def post_message_templates_payload(subject_template: str, content_template: str, provider_id: int) -> list:
        payload = [
            {
                "description": f"Описание сообщения-{fake_ru.bban()}",
                "subject": subject_template,
                "content": content_template,
                "contentTypeID": 2,
                "providerID": provider_id
            }
        ]
        return payload