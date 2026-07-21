import allure
import pytest
from http import HTTPStatus

from services.cards.card_designsettings_by_id.api_card_designsettings_by_id import (
    CardDesignsettingsByIdAPI,
)
from services.cards.card_designsettings_update.api_card_designsettings_update import (
    CardDesignsettingsUpdateAPI,
)
from services.cards.card_designsettings_update.payloads import Payloads
from services.fonts.fonts_list.api_fonts_list import FontsListAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/designsettings — FontColor / FontStyleID (REQUIREMENT 30986)
    """
)
class TestCardsDesignsettingsFont:
    @allure.title("PUT designsettings with FontColor + FontStyleID -> GET reflects fontColor + fontStyle")
    @pytest.mark.smoke
    def test_designsettings_font_color_and_style_merge(self, created_card):
        card_id = created_card.id
        fonts = FontsListAPI().get_fonts()
        assert fonts.items, "No fonts available to test against"
        font = fonts.items[0]

        payload = Payloads.build_card_designsettings_font_payload(
            font_color="AA11BB", font_style_id=font.id
        )
        response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(card_id, payload)
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )

        fetched = CardDesignsettingsByIdAPI().get_card_designsettings_by_id(card_id)
        assert fetched.fontColor == "AA11BB"
        assert fetched.fontStyle is not None
        assert fetched.fontStyle.id == font.id
        assert fetched.fontStyle.fontFamily == font.fontFamily
        assert fetched.fontStyle.url == font.url

    @allure.title("PUT designsettings with only FontColor -> GET reflects fontColor, fontStyle stays unset")
    def test_designsettings_font_color_only(self, created_card):
        card_id = created_card.id

        response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(
            card_id, {"fontColor": "112233"}
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )

        fetched = CardDesignsettingsByIdAPI().get_card_designsettings_by_id(card_id)
        assert fetched.fontColor == "112233"
        assert fetched.fontStyle is None

    @allure.title("PUT designsettings resets FontColor/FontStyleID with null -> GET no longer returns them")
    def test_designsettings_font_reset_with_null(self, created_card):
        card_id = created_card.id
        fonts = FontsListAPI().get_fonts()
        assert fonts.items, "No fonts available to test against"
        font = fonts.items[0]

        payload = Payloads.build_card_designsettings_font_payload(
            font_color="CCDDEE", font_style_id=font.id
        )
        set_response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(card_id, payload)
        assert set_response.status_code == HTTPStatus.ACCEPTED

        reset_response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(
            card_id, {"fontColor": None, "fontStyleID": None}
        )
        assert reset_response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {reset_response.status_code}: {reset_response.text}"
        )

        fetched = CardDesignsettingsByIdAPI().get_card_designsettings_by_id(card_id)
        assert fetched.fontColor is None
        assert fetched.fontStyle is None

    @allure.title("PUT designsettings with FontColor longer than 6 chars -> 409")
    @pytest.mark.ng
    def test_designsettings_font_color_too_long(self, created_card):
        card_id = created_card.id

        response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(
            card_id, {"fontColor": "TOOLONGHEX"}
        )
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data[0]["code"] == "InvalidData", f"Expected code=InvalidData, got: {data}"

    @allure.title("PUT designsettings with FontStyleID out of Int16 range -> 400")
    @pytest.mark.ng
    def test_designsettings_font_style_id_out_of_range(self, created_card):
        card_id = created_card.id

        response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(
            card_id, {"fontStyleID": 999999}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Expected HTTPStatus.BAD_REQUEST, got {response.status_code}: {response.text}"
        )

    @allure.title("PUT designsettings with nonexistent FontStyleID -> 409")
    @pytest.mark.ng
    def test_designsettings_font_style_id_nonexistent(self, created_card):
        card_id = created_card.id

        response = CardDesignsettingsUpdateAPI().merge_card_designsettings_raw(
            card_id, {"fontStyleID": 9999}
        )
        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data[0]["code"] == "InvalidData", f"Expected code=InvalidData, got: {data}"

    @allure.title("GET designsettings for a fresh card has no font fields set")
    def test_designsettings_font_default_empty_for_new_card(self, created_card):
        fetched = CardDesignsettingsByIdAPI().get_card_designsettings_by_id(created_card.id)
        assert fetched.fontColor is None
        assert fetched.fontStyle is None
