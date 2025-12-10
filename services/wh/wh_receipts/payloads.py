

class Payloads:

    @staticmethod
    def post_add_receipt_payload(wh_id: int, wh_status_id: int, erp_name: str, number: str, operation_type_id: int) -> list:
        payload = [
            {
                "number": number,
                "warehouseID": wh_id,
                "documentStatusID": wh_status_id,
                "erpID": erp_name,
                "operationTypeID": operation_type_id
            }
        ]
        return payload

    @staticmethod
    def post_add_receipts_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def put_update_receipts_payload(*data: tuple) -> list:
        return [*data]

    @staticmethod
    def put_restore_receipts_payload(*receipts_ids: int) -> list:
        return [*receipts_ids]

    @staticmethod
    def post_add_receipt_negative_payload(*data: dict) -> list:
        return [*data]

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
