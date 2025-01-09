
class Payloads:

    @staticmethod
    def post_add_task_attributes_payload(
            task_id: int,
            attribute_id: int,
            value: str
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "attributeID": attribute_id,
                        "value": value
                    }
                ]
            }
        ]
        return payload
