from src.constants.attributes import PHONE_ATTRIBUTE_ID


class Payloads:
    @staticmethod
    def build_card_attributes_merge_payload(
        attribute_id: int = PHONE_ATTRIBUTE_ID,
        value: str = "+79000000001",
    ) -> list[dict]:
        return [
            {
                "AttributeID": attribute_id,
                "Name": "Phone",
                "SortOrder": 1,
                "Value": [value],
                "IsEnabled": True,
                "AttributeFormID": None,
            }
        ]
