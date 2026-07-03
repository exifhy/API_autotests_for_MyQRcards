

class Payloads:

    @staticmethod
    def post_add_trigger_recipient_selection_rules_payload(
        trigger_id: int,
        recipient_selection_rule_id: int
    ) -> list:
        payload = [
            {
                "triggerID": trigger_id,
                "data": [
                    recipient_selection_rule_id
                ]
            }
        ]
        return payload