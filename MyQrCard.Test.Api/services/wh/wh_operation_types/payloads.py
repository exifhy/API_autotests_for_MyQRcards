

class Payloads:

    @staticmethod
    def post_operation_type_payload(name: str, doc_type_id: int, erp_id: str) -> list:
        payload = [
            {
                "name": name,
                "documentTypeID": doc_type_id,
                "erpID": erp_id
            }
        ]
        return payload


    @staticmethod
    def put_operation_type_payload(name: str, doc_type_id: int, erp_id: str, type_id: int) -> list:
        payload = [
            {
                "name": name,
                "documentTypeID": doc_type_id,
                "erpID": erp_id,
                "id": type_id
            }
        ]
        return payload