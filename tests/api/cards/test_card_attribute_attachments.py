import allure
import pytest
from http import HTTPStatus

from services.cards.card_attribute_attachments.api_card_attribute_attachments import CardAttributeAttachmentsAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    GET /cards/{id}/attributes/attachments
    """
)
class TestCardAttributeAttachments:
    @allure.title("GET /cards/{id}/attributes/attachments")
    @pytest.mark.smoke
    def test_card_attribute_attachments_200(self, created_card):
        response, model = CardAttributeAttachmentsAPI().get_card_attribute_attachments(created_card.id)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)

    @pytest.mark.ng
    @allure.title("GET /cards/{id}/attributes/attachments without auth -> 401/403")
    def test_card_attribute_attachments_401_without_auth(self, created_card):
        response = CardAttributeAttachmentsAPI().get_card_attribute_attachments_without_auth(created_card.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
