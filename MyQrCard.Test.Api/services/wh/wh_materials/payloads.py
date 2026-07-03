

class Payloads:

    @staticmethod
    def post_add_materials_payload(name: str, currency_id: int, unit_id: int, erp_name: str) -> list:
        payload = [
            {
                "name": name,
                "erpID": erp_name,
                "measurementUnitID": unit_id,
                "Cost": 10.50,
                "costCurrencyID": currency_id,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": currency_id,
            }
        ]
        return payload

    @staticmethod
    def post_add_three_materials_payload(*data) -> list:
        return [*data]

    @staticmethod
    def put_update_material_payload(*data) -> list:
        return [*data]

    @staticmethod
    def put_update_materials_payload(
            material_id: int, name: str, currency_id: int, unit_id: int, erp_name: str
    ) -> list:
        payload = [
            {
                "id": material_id,
                "name": name,
                "erpID": erp_name,
                "measurementUnitID": unit_id,
                "Cost": 10.50,
                "costCurrencyID": currency_id,
                "PurchaseCost": 10.50,
                "purchaseCostCurrencyID": currency_id,
            }
        ]
        return payload

    @staticmethod
    def delete_materials_by_list(*materials_ids) -> list:
        return [*materials_ids]

    @staticmethod
    def post_attachments_to_material_by_list_payload(*attachments_ids: int) -> list:
        return [*attachments_ids]

    @staticmethod
    def delete_attachments_from_material_by_list_payload(*attachments_ids: int) -> list:
        return [*attachments_ids]

    @staticmethod
    def post_add_barcodes_material_payload(material_id: int, *data: dict) -> list:
        payload = [
            {
                "materialID": material_id,
                "barcodes": [*data]
            }
        ]
        return payload

    @staticmethod
    def put_update_material_barcode_payload(
            material_id: int, barcode_id: int, barcode_type_id: int, value: str
    ) -> list:
        payload = [
            {
                "materialID": material_id,
                "barcodes": [
                    {
                        "id": barcode_id,
                        "barcodeTypeID": barcode_type_id,
                        "value": value
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_barcodes_from_material_by_list_payload(material_id: int, *barcodes_ids: int) -> list:
        payload = [
            {
                "data": [
                    *barcodes_ids
                ],
                "materialID": material_id
            }
        ]
        return payload

    @staticmethod
    def put_materials_restore_by_list_payload(*materials_ids: int) -> list:
        return [*materials_ids]
