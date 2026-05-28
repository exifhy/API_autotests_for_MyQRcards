import allure
import pytest
from http import HTTPStatus

from services.attachments.attachment_by_id.api_attachment_by_id import AttachmentByIdAPI
from services.attachments.attachment_create.api_attachment_create import AttachmentCreateAPI
from services.attachments.attachment_create_v2.api_attachment_create_v2 import AttachmentCreateV2API
from services.attachments.attachment_delete_by_id.api_attachment_delete_by_id import AttachmentDeleteByIdAPI


@allure.epic("API")
@allure.feature("Attachments")
@pytest.mark.api
@allure.description(
    """
    Проверки Attachments API с изображениями, сгенерированными в коде.
    """
)
class TestAttachments:
    @allure.title("POST /Attachments -> DELETE /Attachments/{id}")
    @pytest.mark.smoke
    def test_attachment_create_delete_flow(self):
        created = AttachmentCreateAPI().create_attachment(label="attachments_post_delete")
        assert created.id is not None
        assert created.publicUrl is None or created.publicUrl != ""

        deleted = AttachmentDeleteByIdAPI().delete_attachment_by_id(created.id)
        assert deleted.status_code == HTTPStatus.ACCEPTED

    @allure.title("POST /Attachments/v2 -> DELETE /Attachments/{id}")
    def test_attachment_create_v2_delete_flow(self):
        created = AttachmentCreateV2API().create_attachment_v2(label="attachments_post_v2_delete")
        assert created.attachments, "Expected non-empty attachments array"
        first = created.attachments[0]
        assert first.id is not None
        assert first.url is None or first.url != ""

        deleted = AttachmentDeleteByIdAPI().delete_attachment_by_id(first.id)
        assert deleted.status_code == HTTPStatus.ACCEPTED

    @allure.title("POST /Attachments -> GET /Attachments/{id} -> DELETE /Attachments/{id}")
    def test_attachment_create_get_delete_flow(self):
        created = AttachmentCreateAPI().create_attachment(label="attachments_post_get_delete")
        assert created.id is not None

        fetched = AttachmentByIdAPI().get_attachment_by_id(created.id)
        assert fetched.publicUrl is None or fetched.publicUrl != ""
        assert fetched.internalFileName is None or fetched.internalFileName != ""

        deleted = AttachmentDeleteByIdAPI().delete_attachment_by_id(created.id)
        assert deleted.status_code == HTTPStatus.ACCEPTED
