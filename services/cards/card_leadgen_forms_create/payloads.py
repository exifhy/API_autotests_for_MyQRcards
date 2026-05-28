import time


class Payloads:
    @staticmethod
    def build_card_leadgen_form_create_payload(
        *,
        field_template_id: int,
        custom_message_template_id: int | None = None,
    ) -> dict:
        suffix = int(time.time())
        payload = {
            "formText": f"AT lead form text {suffix}",
            "buttonText": f"AT button {suffix}",
            "fields": [
                {
                    "isVisible": True,
                    "isRequired": True,
                    "sortOrder": 1,
                    "fieldTemplateID": int(field_template_id),
                    "customFieldName": f"AT custom field {suffix}",
                }
            ],
        }
        if custom_message_template_id is not None:
            payload["CustomMessageTemplateID"] = int(custom_message_template_id)
        return payload
