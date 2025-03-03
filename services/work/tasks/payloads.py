

class Payloads:

    @staticmethod
    def add_task_payload(
            criticality_id: str,
            number: str,
            note: str,
            task_type_id: str,
            date: str,
            **kwargs
    ) -> dict:
        payload = {
            "CriticalityID": criticality_id,
            "EstimatedCostCurrencyID": 1,
            "FaultTimestamp": date,
            "RequestMethodID": 1,
            "RequestedFinishDateTime": date,
            "RequestedStartDateTime": date,
            "TaskTypeID": task_type_id,
            "notes": note,
            "number": number,
            **kwargs
        }
        return payload

    @staticmethod
    def put_update_task_payload(
            number: str,
            note: str,
            date: str,
            **kwargs
    ) -> dict:
        payload = {
            "FaultTimestamp": date,
            "RequestedFinishDateTime": date,
            "RequestedStartDateTime": date,
            "notes": note,
            "number": number,
            **kwargs
        }
        return payload

    @staticmethod
    def post_add_conversation_to_task_payload(
            external: bool,
            value: str
    ) -> dict:
        payload = {
            "message": value,
            "isExternal": external,
            "attachments": []
        }
        return payload

    @staticmethod
    def post_add_checklists_to_task_payload(checklist_id: int) -> list:
        payload = [
            {
                "checkListID": checklist_id
            }
        ]
        return payload

    @staticmethod
    def delete_checklists_from_task_by_list_payload(*checklist_ids: int) -> list:
        return [*checklist_ids]

    @staticmethod
    def delete_results_checklist_from_task_by_list_payload(*task_results_checklist_ids: int) -> list:
        return [*task_results_checklist_ids]

    @staticmethod
    def put_update_results_task_checklists_items_v2_payload(
            task_checklist_result_id: str,
            checked: bool,
            value,
            type_item
    ) -> list:
        payload = [
            {
                "id": task_checklist_result_id,
                "isChecked": checked,
                "type": type_item,
                "values": [
                    value
                ]
            }
        ]
        return payload

    @staticmethod
    def put_update_attributes_task_completed_work_by_id_payload(
        attribute_id: int,
        value: str
    ) -> list:
        payload = [
            {
                "attributeID": attribute_id,
                "value": [
                    value
                ]
            }
        ]
        return payload

    @staticmethod
    def put_update_attributes_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        attribute_id: int,
        value: str
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "completedWorkID": completed_work_id,
                "data": [
                    {
                        "isPublic": True,
                        "attributeID": attribute_id,
                        "value": [
                            value
                        ]
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_attributes_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        *attribute_ids: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "completedWorkID": completed_work_id,
                "data": [
                    *attribute_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_attributes_task_completed_work_by_list_payload(*attribute_ids: int) -> list:
        return [*attribute_ids]

    @staticmethod
    def post_add_materials_to_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        material_id: int,
        warehouse_id: int,
        inventory_id: int,
        measurement_unit_id: int,
        qty: int,
        user_id: int,
        cost: int,
        currency: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "materials": [
                            {
                                "materialID": material_id,
                                "warehouseID": warehouse_id,
                                "inventoryID": inventory_id,
                                "measurementUnitID": measurement_unit_id,
                                "quantity": qty,
                                "consumedByUserID": user_id,
                                "cost": cost,
                                "costCurrencyID": currency
                            }
                        ]
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def post_add_technicians_to_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        rate: int,
        user_id: int,
        currency: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "technicians": [
                            {
                                "userID": user_id,
                                "rate": rate,
                                "rateCurrencyID": currency
                            }
                        ]
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_materials_task_completed_work_payload(
        material_id: int,
        wh_id: int,
        inventory_id: int,
    ) -> dict:
        payload = {
            "materialID": material_id,
            "warehouseID": wh_id,
            "inventoryID": inventory_id
        }
        return payload

    @staticmethod
    def put_update_materials_to_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        material_id: int,
        warehouse_id: int,
        inventory_id: int,
        measurement_unit_id: int,
        qty: int,
        user_id: int,
        cost: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "materials": [
                            {
                                "materialID": material_id,
                                "warehouseID": warehouse_id,
                                "inventoryID": inventory_id,
                                "measurementUnitID": measurement_unit_id,
                                "quantity": qty,
                                "consumedByUserID": user_id,
                                "cost": cost,
                            }
                        ]
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_materials_from_task_completed_works_payload(
        task_id: int,
        completed_work_id: int,
        material_id: int,
        warehouse_id: int,
        inventory_id: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "materials": [
                            {
                                "materialID": material_id,
                                "warehouseID": warehouse_id,
                                "inventoryID": inventory_id,
                            }
                        ]
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def post_add_uploaded_signature_to_report_task_completed_works_v2_payload(
        job_title: str,
        signatory: str
    ) -> dict:
        payload = {
            "jobTitle": job_title,
            "signatory": signatory

        }
        return payload

    @staticmethod
    def delete_technicians_task_completed_works_by_list_payload(*technicians_ids: int) -> list:
        return [*technicians_ids]

    @staticmethod
    def put_update_technician_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        rate: int,
        user_id: int,
        currency: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "technicians": [
                            {
                                "userID": user_id,
                                "rate": rate,
                                "rateCurrencyID": currency
                            }
                        ]
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_technician_from_task_completed_work_payload(
        task_id: int,
        completed_work_id: int,
        *user_ids: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "technicians": [
                                *user_ids
                        ]
                    }
                ]
            }
        ]
        return payload
