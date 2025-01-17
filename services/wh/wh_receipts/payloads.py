

class Payloads:

    @staticmethod
    def post_add_receipt_payload(wh_id: int, wh_status_id: int, erp_name: str) -> list:
        payload = [
            {
                "warehouseID": wh_id,
                "documentStatusID": wh_status_id,
                "erpID": erp_name
            }
        ]
        return payload

    @staticmethod
    def delete_receipts_payload(*receipt_ids: tuple) -> list:
        return [*receipt_ids]

    @staticmethod
    def delete_items_receipts_payload(receipt_id: int, *items_ids: tuple) -> list:
        payload = [
            {
                "receiptID": receipt_id,
                "items": [
                    *items_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def post_add_items_receipt_payload(receipt_id: int, material_id: int, unit_id: int, qty: int) -> list:
        payload = [
            {
                "receiptID": receipt_id,
                "items": [
                    {
                        "materialID": material_id,
                        "measurementUnitID": unit_id,
                        "quantity": qty
                    }
                ]
            }
        ]
        return payload
