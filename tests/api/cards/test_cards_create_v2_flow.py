import allure
import pytest

from services.attachments.attachment_create.api_attachment_create import AttachmentCreateAPI
from services.attachments.attachment_delete_by_id.api_attachment_delete_by_id import AttachmentDeleteByIdAPI
from services.cards.card_by_id_v2.api_card_by_id_v2 import CardByIdV2API
from services.cards.card_create_v2.api_card_create_v2 import CardCreateV2API


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/V2.0
    """
)
class TestCardsCreateV2Flow:
    @allure.title("POST /Cards/V2.0 -> GET /Cards/{id}/V2")
    @pytest.mark.smoke
    def test_cards_create_v2_flow(self):
        attachment = AttachmentCreateAPI().create_attachment(label="card_create_v2")
        assert attachment.id is not None
        try:
            created = CardCreateV2API().create_card_v2(attachment_id=attachment.id)
            assert created.id is not None

            fetched = CardByIdV2API().get_card_by_id_v2(created.id)
            assert fetched.id == created.id
            assert fetched.person is not None
            assert fetched.person.firstName is not None and fetched.person.firstName != ""
            assert fetched.name is not None and fetched.name != ""
        finally:
            try:
                AttachmentDeleteByIdAPI().delete_attachment_by_id(attachment.id)
            except Exception:
                pass
