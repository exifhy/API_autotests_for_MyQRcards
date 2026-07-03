from config.config import HOST


class Endpoints:

    @staticmethod
    def get_task_assignments_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/assignments'

    @staticmethod
    def get_task_attachments_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/attachments'

    @staticmethod
    def get_task_attachment_by_id_endpoint(task_id: int, attachment_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/attachment/{attachment_id}'

    @staticmethod
    def get_task_attachments_by_id_temporary_redirect_endpoint(task_id: int, attachment_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/attachments/{attachment_id}'

    @staticmethod
    def get_task_attributes_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/attributes'

    get_task_change_types_endpoint = f'{HOST}/WORK/tasks/changeTypes'

    @staticmethod
    def get_task_changes_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/changes'

    @staticmethod
    def get_task_checklists_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists'

    @staticmethod
    def post_add_checklists_to_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists'

    @staticmethod
    def delete_checklists_from_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists'

    @staticmethod
    def post_add_checklists_to_task_by_id_endpoint(task_id: int, task_checklist_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}'

    @staticmethod
    def delete_checklist_from_task_by_id_endpoint(task_id: int, task_checklist_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}'

    @staticmethod
    def get_list_attachments_checklist_from_task_by_id_endpoint(
            task_id: int,
            task_checklist_id: int,
            task_checklist_result_id: int
    ) -> str:
        return (f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}/'
                f'results/{task_checklist_result_id}/attachments')

    @staticmethod
    def get_list_attachments_checklist_from_task_endpoint(task_id: int, task_checklist_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}/results/attachments'

    @staticmethod
    def get_attachment_by_id_checklist_from_task_by_id_endpoint(
            task_id: int,
            task_checklist_id: int,
            task_checklist_result_id: int,
            attachment_id: int
    ) -> str:
        return (f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}/results/'
                f'{task_checklist_result_id}/attachments/{attachment_id}')

    @staticmethod
    def post_upload_attachment_to_server_bind_to_checklist_task_from_form_endpoint(
            task_id: int,
            checklist_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{checklist_id}/upload/fromForm'

    @staticmethod
    def delete_results_checklist_from_task_endpoint(
            task_id: int,
            task_checklist_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}/results'

    @staticmethod
    def get_results_checklist_from_task_v2_endpoint(
            task_id: int,
            task_checklist_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}/results/v2'

    @staticmethod
    def put_results_checklist_from_task_v2_endpoint(
            task_id: int,
            task_checklist_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkLists/{task_checklist_id}/results/v2'

    @staticmethod
    def get_list_files_attached_to_attribute_by_id_of_completed_work_by_id_on_task_endpoint(
            task_id: int,
            completed_work_id: int,
            attribute_id: int,
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attributes/{attribute_id}/attachments'

    @staticmethod
    def get_list_files_attached_to_attribute_of_completed_work_by_id_on_task_endpoint(
            task_id: int,
            completed_work_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attributes/attachments'

    @staticmethod
    def post_upload_file_to_server_bind_to_completed_work_from_form_endpoint(
            task_id: int,
            completed_work_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/upload/fromForm'

    @staticmethod
    def get_attributes_for_completed_work_from_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/attributes'

    @staticmethod
    def get_attributes_for_completed_work_by_id_from_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attributes'

    @staticmethod
    def put_update_attributes_for_completed_work_by_id_from_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attributes'

    @staticmethod
    def delete_attributes_from_completed_work_by_id_from_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attributes'

    put_update_attributes_completed_work_by_task_endpoint = f'{HOST}/WORK/tasks/completedWorks/attributes'
    delete_attributes_completed_work_by_task_endpoint = f'{HOST}/WORK/tasks/completedWorks/attributes'

    @staticmethod
    def delete_attribute_by_id_completed_work_by_id_from_task_endpoint(
            task_id: int,
            completed_work_id: int,
            attribute_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attributes/{attribute_id}'

    @staticmethod
    def get_completed_work_from_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks'

    @staticmethod
    def get_completed_work_by_id_from_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}'

    @staticmethod
    def get_attachments_from_completed_work_by_id_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attachments'

    @staticmethod
    def get_list_attachments_from_completed_work_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/attachments'

    @staticmethod
    def get_temporary_redirect_attachments_completed_work_by_id_task_endpoint(
            task_id: int,
            completed_work_id: int,
            attachment_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/attachments/{attachment_id}'

    @staticmethod
    def get_list_materials_from_completed_work_by_id_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/materials'

    @staticmethod
    def delete_materials_from_completed_work_by_id_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/materials'

    @staticmethod
    def get_materials_from_completed_work_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/materials'

    put_update_materials_from_completed_work_task_endpoint = f'{HOST}/WORK/tasks/completedWorks/materials'
    post_add_materials_from_completed_work_task_endpoint = f'{HOST}/WORK/tasks/completedWorks/materials'
    delete_materials_from_completed_work_task_endpoint = f'{HOST}/WORK/tasks/completedWorks/materials'

    @staticmethod
    def get_report_attachment_from_completed_work_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/report/attachment'

    @staticmethod
    def post_add_attachment_by_id_report_completed_work_task_endpoint(task_id: int, attachment_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/report/attachment/{attachment_id}'

    @staticmethod
    def post_add_attachment_by_id_report_completed_work_task_v2_endpoint(task_id: int, attachment_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/report/attachment/v2/{attachment_id}'

    @staticmethod
    def delete_attachment_by_id_report_completed_work_task_endpoint(task_id: int, attachment_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/report/attachment/{attachment_id}'

    post_upload_attachment_bind_to_report_completed_work_task_from_form_endpoint = \
        f'{HOST}/WORK/tasks/completedWorks/report/attachment/upload/fromForm'
    post_upload_attachment_bind_to_report_completed_work_task_from_body_endpoint = \
        f'{HOST}/WORK/tasks/completedWorks/report/attachment/upload/fromBody'

    @staticmethod
    def get_list_technicians_from_completed_work_by_id_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/technicians'

    @staticmethod
    def delete_technicians_from_completed_work_task_endpoint(task_id: int, completed_work_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/{completed_work_id}/technicians'

    @staticmethod
    def get_list_technicians_from_completed_work_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/completedWorks/technicians'

    put_update_technicians_from_completed_works_task_endpoints = f'{HOST}/WORK/tasks/completedWorks/technicians'
    post_add_technicians_to_completed_works_task_endpoints = f'{HOST}/WORK/tasks/completedWorks/technicians'
    delete_technicians_from_completed_works_task_endpoints = f'{HOST}/WORK/tasks/completedWorks/technicians'

    @staticmethod
    def get_list_contacts_from_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/contacts'

    @staticmethod
    def get_contact_by_id_from_task_endpoint(task_id: int, contact_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/contacts/{contact_id}'

    @staticmethod
    def delete_contact_by_id_from_task_endpoint(task_id: int, contact_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/contacts/{contact_id}'

    @staticmethod
    def get_conversations_from_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/conversations'

    @staticmethod
    def head_conversations_from_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/conversations'

    @staticmethod
    def get_conversation_by_id_from_task_endpoint(task_id: int, task_conversation_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/conversations/{task_conversation_id}'

    @staticmethod
    def post_add_conversation_to_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/Tasks/{task_id}/conversation'

    @staticmethod
    def get_temporary_redirect_attachment_conversations_task_endpoint(
            task_id: int,
            task_conversation_id: int,
            attachment_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/conversations/{task_conversation_id}/attachments/{attachment_id}'

    @staticmethod
    def get_conversation_delivery_status_task_endpoint(
            task_id: int,
            task_conversation_id: int
    ) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/conversations/{task_conversation_id}/delivery'

    @staticmethod
    def post_upload_attachments_to_conversation_task_from_form_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/conversation/upload/fromForm'

    @staticmethod
    def get_detailed_info_task_by_id_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}'

    @staticmethod
    def put_update_task_by_id_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}'

    @staticmethod
    def delete_task_by_id_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}'

    @staticmethod
    def patch_task_by_id_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}'

    @staticmethod
    def get_check_company_code_used_task_by_id_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/checkCompanyCodeUsed'

    get_list_task_endpoint = f'{HOST}/WORK/tasks'
    post_add_task_endpoint = f'{HOST}/WORK/tasks'
    delete_task_endpoint = f'{HOST}/WORK/tasks'
    head_task_endpoint = f'{HOST}/WORK/tasks'
    get_short_list_task_endpoint = f'{HOST}/WORK/tasks/short'

    @staticmethod
    def put_mark_task_as_completed_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/complete'

    put_restore_task_endpoint = f'{HOST}/WORK/tasks/restore'
    get_count_task_by_day_endpoint = f'{HOST}/WORK/tasks/count'
    get_short_list_of_task_clustered_by_geo_hash_endpoint = f'{HOST}/WORK/tasks/groupBy/geoHash'

    @staticmethod
    def get_list_materials_for_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/materials'

    @staticmethod
    def get_meta_data_for_form_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/meta'

    get_meta_new_data_for_form_task_endpoint = f'{HOST}/WORK/tasks/new/meta'

    @staticmethod
    def get_ratings_avg_engineers_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/ratings/avg'

    @staticmethod
    def get_ratings_engineers_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/ratings'

    @staticmethod
    def get_skills_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/skills'

    @staticmethod
    def post_activate_auto_staginging_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/autoStaginging'

    @staticmethod
    def delete_deactivate_auto_staginging_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/autoStaginging'

    @staticmethod
    def get_history_stages_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/stages'

    @staticmethod
    def get_list_of_available_stages_to_task_can_transferred_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/stages/next'

    get_available_next_stages_to_task_from_list_endpoint = f'{HOST}/WORK/tasks/stages/next'

    @staticmethod
    def get_tags_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/tags'

    @staticmethod
    def get_watch_list_by_task_endpoint(task_id: int) -> str:
        return f'{HOST}/WORK/tasks/{task_id}/watchLists'
