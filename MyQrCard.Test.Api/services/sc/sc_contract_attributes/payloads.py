

class Payloads:

    @staticmethod
    def post_updates_info_about_custom_object_attributes_payload(
            contract_id: int,
            attribute_value: str,
            attribute_id: str,
            **kwargs
    ) -> list:
        """post_updates_info_about_custom_object_attributes(1, 'asd', '1', **params)"""
        payload = [
            {
                "contractID": contract_id,
                "data": [
                    {
                        "isPublic": True,
                        "value": [attribute_value],
                        "attributeID": attribute_id
                    }
                ]
            }
        ]
        if kwargs:
            payload.append(kwargs)
        return payload
