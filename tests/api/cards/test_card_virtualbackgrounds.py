import allure
import pytest

from services.cards.card_virtualbackgrounds.api_card_virtualbackgrounds import CardVirtualBackgroundsAPI
from services.cards.card_virtualbackgrounds_add.api_card_virtualbackgrounds_add import CardVirtualBackgroundsAddAPI
from services.cards.card_virtualbackgrounds_remove.api_card_virtualbackgrounds_remove import (
    CardVirtualBackgroundsRemoveAPI,
)
from services.virtual_backgrounds.virtual_backgrounds_list.api_virtual_backgrounds import VirtualBackgroundsAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    GET /Cards/{card_id}/virtualbackground
    POST /Cards/{card_id}/virtualbackground
    DELETE /Cards/{card_id}/virtualbackground
    """
)
class TestCardVirtualBackgrounds:
    @allure.title("GET /Cards/{card_id}/virtualbackground returns list")
    def test_card_virtualbackgrounds_200(self, created_card):
        _, model = CardVirtualBackgroundsAPI().get_card_virtualbackgrounds(int(created_card.id))
        assert isinstance(model.items, list)

    @allure.title("POST add → GET verify present → DELETE remove → GET verify absent")
    def test_card_virtualbackgrounds_add_remove_flow(self, created_card):
        card_id = int(created_card.id)

        with allure.step("GET /VirtualBackgrounds — pick first available background"):
            _, bg_model = VirtualBackgroundsAPI().get_virtual_backgrounds(offset=0, fetch=10)
            if not bg_model.items or bg_model.items[0].id is None:
                pytest.skip("No virtual backgrounds available in the system")
            background_id = int(bg_model.items[0].id)

        with allure.step(f"POST — add background id={background_id} to card"):
            CardVirtualBackgroundsAddAPI().add_card_virtualbackgrounds(card_id, [background_id])

        with allure.step("GET — verify background is present on card"):
            _, card_bg_model = CardVirtualBackgroundsAPI().get_card_virtualbackgrounds(card_id)
            present_ids = [int(item.id) for item in card_bg_model.items if item.id is not None]
            assert background_id in present_ids, f"Background {background_id} not found after add: {present_ids}"

        with allure.step(f"DELETE — remove background id={background_id} from card"):
            CardVirtualBackgroundsRemoveAPI().remove_card_virtualbackgrounds(card_id, [background_id])

        with allure.step("GET — verify background is absent from card"):
            _, card_bg_model_after = CardVirtualBackgroundsAPI().get_card_virtualbackgrounds(card_id)
            remaining_ids = [int(item.id) for item in card_bg_model_after.items if item.id is not None]
            assert background_id not in remaining_ids, f"Background {background_id} still present after remove"
