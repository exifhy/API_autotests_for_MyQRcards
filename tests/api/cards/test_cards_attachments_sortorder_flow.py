import allure
import pytest
from http import HTTPStatus

from services.attachments.attachment_create.api_attachment_create import AttachmentCreateAPI
from services.attachments.attachment_delete_by_id.api_attachment_delete_by_id import AttachmentDeleteByIdAPI
from services.cards.card_attachments_sortorder.api_card_attachments_sortorder import CardAttachmentsSortOrderAPI
from services.cards.card_update_v2.api_card_update_v2 import CardUpdateV2API
from tests.api.cards.helpers import (
    wait_card_attachments_sortorder,
    wait_card_v2_gallery_contains,
)


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/attachments/sortorder
    """
)
class TestCardsAttachmentsSortOrderFlow:
    @allure.title("POST /Cards -> PUT /Cards/{id}/V2 gallery -> GET/PUT /Cards/{id}/attachments/sortorder")
    @pytest.mark.smoke
    def test_cards_attachments_sortorder_flow(self, created_card, cfg):
        created = created_card

        first_attachment = AttachmentCreateAPI().create_attachment(label="card_sortorder_1")
        second_attachment = AttachmentCreateAPI().create_attachment(label="card_sortorder_2")
        attachment_ids = [first_attachment.id, second_attachment.id]
        assert all(attachment_ids)
        try:
            updated_response, _ = CardUpdateV2API().update_card_v2(
                created.id,
                company_id=cfg["company_id_create"],
                gallery_attachment_ids=[int(first_attachment.id), int(second_attachment.id)],
            )
            assert updated_response.status_code == HTTPStatus.ACCEPTED

            card_with_gallery = wait_card_v2_gallery_contains(
                created.id,
                [int(first_attachment.id), int(second_attachment.id)],
            )
            assert card_with_gallery is not None

            response, items = CardAttachmentsSortOrderAPI().get_card_attachments_sortorder(created.id)
            assert response.status_code == HTTPStatus.OK
            got_attachment_ids = {item.attachmentID for item in items if item.attachmentID is not None}
            assert {int(first_attachment.id), int(second_attachment.id)}.issubset(got_attachment_ids)

            _, payload = CardAttachmentsSortOrderAPI().update_card_attachments_sortorder(
                created.id,
                {"attachmentID": int(second_attachment.id), "sortOrder": 1},
                {"attachmentID": int(first_attachment.id), "sortOrder": 2},
            )

            expected = {entry["attachmentID"]: entry["sortOrder"] for entry in payload}
            matched = wait_card_attachments_sortorder(created.id, expected)
            assert matched is not None
        finally:
            for attachment_id in reversed(attachment_ids):
                try:
                    AttachmentDeleteByIdAPI().delete_attachment_by_id(attachment_id)
                except Exception:
                    pass
