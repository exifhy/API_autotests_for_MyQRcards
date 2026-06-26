import allure
import pytest
from http import HTTPStatus

from services.attachments.attachment_upload_cdn.api_attachment_upload_cdn import AttachmentUploadCdnAPI
from src.utils.image_factory import generate_image_bytes, generate_large_image_bytes


@allure.epic("API")
@allure.feature("Attachments CDN")
@pytest.mark.api
@allure.description(
    """
    Проверки нового CDN endpoint загрузки файлов.
    dev:  https://dev-upload.myqrcards.com/attachments/v2/
    prod: https://upload.myqrcards.com/attachments/v2/
    """
)
class TestAttachmentUploadCdn:

    @allure.title("POST /attachments/v2/ (CDN) — файл < 1МБ → 200/201")
    @pytest.mark.smoke
    def test_cdn_upload_small_file(self):
        generated = generate_image_bytes(fmt="png", label="cdn_upload_small")
        response = AttachmentUploadCdnAPI().upload_attachment_cdn(generated)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"CDN upload failed: {response.status_code} {response.text}"
        )

    @allure.title("POST /attachments/v2/ (CDN) — файл > 2МБ → 200/201")
    @pytest.mark.smoke
    def test_cdn_upload_large_file(self):
        generated = generate_large_image_bytes(target_size_mb=2.0)
        response = AttachmentUploadCdnAPI().upload_attachment_cdn(generated)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"CDN large upload failed: {response.status_code} {response.text}"
        )

