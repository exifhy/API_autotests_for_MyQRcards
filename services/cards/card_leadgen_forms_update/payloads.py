import time


class Payloads:
    @staticmethod
    def build_card_leadgen_forms_update_payload(
        *,
        leadgen_form_id: int,
        field_template_id: int,
        custom_message_template_id: int | None = None,
    ) -> list[dict]:
        suffix = int(time.time())
        payload_item = {
            "id": int(leadgen_form_id),
            "formText": f"AT updated lead form text {suffix}",
            "buttonText": f"AT updated button {suffix}",
            "fields": [
                {
                    "isVisible": True,
                    "isRequired": True,
                    "sortOrder": 1,
                    "fieldTemplateID": int(field_template_id),
                    "customFieldName": f"AT updated custom field {suffix}",
                }
            ],
        }
        if custom_message_template_id is not None:
            payload_item["CustomMessageTemplateID"] = int(custom_message_template_id)
        return [payload_item]
