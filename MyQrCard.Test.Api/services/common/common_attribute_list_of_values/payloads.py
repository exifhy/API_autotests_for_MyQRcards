

class Payloads:

    @staticmethod
    def post_add_attribute_list_of_value_payload(attribute_id: int, *args) -> list:
        payload = [
            {
                "attributeID": attribute_id,
                "data": [
                    *args
                ]
            }
        ]
        return payload
