

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
    def delete_materials_by_list(*materials_ids: tuple) -> list:
        return [*materials_ids]
