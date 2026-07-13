

class Payloads:

	@staticmethod
	def add_work_type_payload(work_type_name: str, notes: str, status: bool) -> list:
		payload = [
			{
				"name": work_type_name,
				"description": notes,
				"isDefault": status,
				"cost": None
			}
		]
		return payload

	@staticmethod
	def put_update_work_type_payload(
			work_type_id: str, work_type_name: str, notes: str, status: bool
	) -> list:
		payload = [
			{
				"id": work_type_id,
				"name": work_type_name,
				"description": notes,
				"isDefault": status,
				"cost": None
			}
		]
		return payload

	@staticmethod
	def delete_work_types_by_list_payload(*work_type_ids: int) -> list:
		return [*work_type_ids]

	@staticmethod
	def publish_work_types_payload(work_type_id: int) -> list:
		return [work_type_id]

	@staticmethod
	def unpublish_work_types_payload(work_type_id: int) -> list:
		return [work_type_id]

	@staticmethod
	def post_add_check_lists_to_work_type_payload(*check_list_ids: int) -> list:
		return [*check_list_ids]

	@staticmethod
	def delete_check_lists_from_work_type_payload(*check_list_ids: int) -> list:
		return [*check_list_ids]

	@staticmethod
	def post_add_task_types_to_work_types_payload(*task_type_ids: int) -> list:
		return [*task_type_ids]

	@staticmethod
	def delete_task_types_from_work_types_payload(*task_type_ids: int) -> list:
		return [*task_type_ids]
