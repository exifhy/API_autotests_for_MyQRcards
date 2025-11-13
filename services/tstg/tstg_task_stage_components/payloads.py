

class Payloads:
    
    def post_task_stage_components_rw_payload(self, task_stage_id: int, attribute_id: int, role_id: int) -> list:
        payload = [
            {
                "taskStageID": task_stage_id,
                "attributes": [
                    {
                        "id": attribute_id,
                        "roleID": role_id,
                        "capabilityID": "2"
                    }
                ]
            }
        ]
        return payload