

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
	def delete_work_types_payload(work_type_id: int) -> list:
		return [work_type_id]

	@staticmethod
	def publish_work_types_payload(work_type_id: int) -> list:
		return [work_type_id]

	@staticmethod
	def unpublish_work_types_payload(work_type_id: int) -> list:
		return [work_type_id]


