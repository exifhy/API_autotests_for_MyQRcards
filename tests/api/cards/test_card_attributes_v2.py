import allure
import pytest
from http import HTTPStatus

from services.cards.card_attributes_delete_v2.api_card_attributes_delete_v2 import CardAttributesDeleteV2API
from services.cards.card_attributes_list.api_card_attributes_list import CardAttributesListAPI
from services.cards.card_attributes_list_v2.api_card_attributes_list_v2 import CardAttributesListV2API
from services.cards.card_attributes_merge.api_card_attributes_merge import CardAttributesMergeAPI
from services.cards.card_attributes_merge_v2.api_card_attributes_merge_v2 import CardAttributesMergeV2API
from services.cards.card_attributes_merge_v2.payloads import Payloads
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_link_attributes_v2.api_card_link_attributes_v2 import CardLinkAttributesV2API
from src.constants.attributes import EMAIL_ATTRIBUTE_ID, PHONE_ATTRIBUTE_ID, TEXT_ATTRIBUTE_ID
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/attributes/V2 (REQUIREMENT 32324) — вложенные дополнительные поля,
    parent-child дерево. Плюс регрессия v1 (/cards/{id}/attributes без /V2).
    """
)
class TestCardAttributesV2:
    @allure.title("PUT /attributes/V2 создаёт дерево -> плоский список с cardAttributeNodeID у каждого узла")
    @pytest.mark.smoke
    def test_v2_merge_creates_tree_flat_response(self, created_card):
        response, items = CardAttributesMergeV2API().merge_card_attributes_v2(created_card.id)

        assert response.status_code == HTTPStatus.ACCEPTED
        assert len(items) == 2, "Expected 2 created nodes (root + child) in the flat PUT response"
        assert all(item.cardAttributeNodeID is not None for item in items), (
            "Every created node must have a cardAttributeNodeID"
        )

    @allure.title("GET /attributes/V2 возвращает настоящее дерево (children, parentCardAttributeNodeID)")
    @pytest.mark.smoke
    def test_v2_get_returns_nested_tree(self, created_card):
        CardAttributesMergeV2API().merge_card_attributes_v2(created_card.id)

        response, roots = CardAttributesListV2API().get_card_attributes_v2(created_card.id)

        assert response.status_code == HTTPStatus.OK
        assert len(roots) == 1
        root = roots[0]
        assert root.parentCardAttributeNodeID is None, (
            "Root node should not have a parentCardAttributeNodeID (field is absent, not present-as-null)"
        )
        assert len(root.children) == 1
        child = root.children[0]
        assert child.parentCardAttributeNodeID == root.cardAttributeNodeID
        assert child.children == []

    @allure.title("Глубина 3 уровня — ок")
    def test_v2_depth_3_levels_ok(self, created_card):
        payload = Payloads.build_nested_chain(3)
        response, items = CardAttributesMergeV2API().merge_card_attributes_v2(created_card.id, payload=payload)

        assert response.status_code == HTTPStatus.ACCEPTED
        assert len(items) == 3

    @allure.title("Глубина 4 уровня (правнук) — 400 PredicateValidator")
    @pytest.mark.ng
    def test_v2_depth_4_levels_400(self, created_card):
        payload = Payloads.build_nested_chain(4)
        response = CardAttributesMergeV2API().merge_card_attributes_v2_raw(created_card.id, payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Expected HTTPStatus.BAD_REQUEST, got {response.status_code}: {response.text}"
        )

    @allure.title("PUT с пустым массивом [] -> 409 (не 400)")
    @pytest.mark.ng
    def test_v2_empty_array_409(self, created_card):
        response = CardAttributesMergeV2API().merge_card_attributes_v2_raw(created_card.id, [])

        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        )

    @allure.title("PUT с телом null -> 400")
    @pytest.mark.ng
    def test_v2_null_body_400(self, created_card):
        response = CardAttributesMergeV2API().merge_card_attributes_v2_raw_body(created_card.id, "null")

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"Expected HTTPStatus.BAD_REQUEST, got {response.status_code}: {response.text}"
        )

    @allure.title("Частичный PUT не удаляет ранее созданные узлы (это не полная замена дерева)")
    def test_v2_partial_put_keeps_existing_nodes(self, created_card):
        card_id = created_card.id

        first_payload = [
            Payloads.build_node(
                TEXT_ATTRIBUTE_ID,
                "Root1",
                sort_order=1,
                children=[Payloads.build_node(PHONE_ATTRIBUTE_ID, "Child-Phone", value=["+79000000001"])],
            ),
            Payloads.build_node(EMAIL_ATTRIBUTE_ID, "Root2-Email", sort_order=2, value=["a@b.com"]),
        ]
        CardAttributesMergeV2API().merge_card_attributes_v2(card_id, payload=first_payload)

        second_payload = [
            Payloads.build_node(EMAIL_ATTRIBUTE_ID, "Root3-New", sort_order=1, value=["c@d.com"]),
        ]
        response, items = CardAttributesMergeV2API().merge_card_attributes_v2(card_id, payload=second_payload)
        assert response.status_code == HTTPStatus.ACCEPTED
        assert len(items) == 1, "Second PUT should only create/touch the one new node it sent"

        _, roots = CardAttributesListV2API().get_card_attributes_v2(card_id)
        assert len(roots) == 3, "Roots from the first PUT must still be there after the partial second PUT"
        root_with_child = next((r for r in roots if len(r.children) == 1), None)
        assert root_with_child is not None, "Root1's child must have survived the partial PUT"

    @allure.title("DELETE родителя каскадно удаляет потомков и пересортировывает соседей")
    def test_v2_delete_cascades_and_resorts_siblings(self, created_card):
        card_id = created_card.id

        payload = [
            Payloads.build_node(
                TEXT_ATTRIBUTE_ID,
                "Root1-WithChild",
                sort_order=1,
                children=[Payloads.build_node(PHONE_ATTRIBUTE_ID, "Child-Phone", value=["+79000000001"])],
            ),
            Payloads.build_node(EMAIL_ATTRIBUTE_ID, "Root2", sort_order=2, value=["a@b.com"]),
            Payloads.build_node(EMAIL_ATTRIBUTE_ID, "Root3", sort_order=3, value=["c@d.com"]),
        ]
        _, items = CardAttributesMergeV2API().merge_card_attributes_v2(card_id, payload=payload)
        root_with_child_id = items[0].cardAttributeNodeID
        child_id = items[1].cardAttributeNodeID

        CardAttributesDeleteV2API().delete_card_attribute_v2(card_id, root_with_child_id)

        _, roots = CardAttributesListV2API().get_card_attributes_v2(card_id)
        remaining_ids = {r.cardAttributeNodeID for r in roots}
        assert root_with_child_id not in remaining_ids, "Deleted root must be gone"
        assert child_id not in remaining_ids, "Deleted root's child must be gone too (cascade)"
        assert len(roots) == 2
        assert sorted(r.sortOrder for r in roots) == [1, 2], "Remaining siblings must be resorted to 1..N"

        # Verify the deleted node's tree is really gone, not just unreachable from the root list
        _, deep_check = CardAttributesListV2API().get_card_attributes_v2(card_id)
        all_ids = {r.cardAttributeNodeID for r in deep_check} | {
            c.cardAttributeNodeID for r in deep_check for c in r.children
        }
        assert child_id not in all_ids

    @allure.title("Публичный GET по cardLink V2 без авторизации совпадает с деревом владельца")
    def test_v2_public_cardlink_get_matches_owner(self, created_card):
        CardAttributesMergeV2API().merge_card_attributes_v2(created_card.id)

        fetched = CardByIdAPI().get_card_by_id(created_card.id)
        assert fetched.url, "Card public url is empty"
        card_link = extract_card_link_id(fetched.url)

        response, public_roots = CardLinkAttributesV2API().get_cardlink_attributes_v2(card_link)
        assert response.status_code == HTTPStatus.OK

        _, owner_roots = CardAttributesListV2API().get_card_attributes_v2(created_card.id)
        assert {r.cardAttributeNodeID for r in public_roots} == {r.cardAttributeNodeID for r in owner_roots}

    @allure.title("Регрессия v1: GET /cards/{id}/attributes/ на визитке с деревом — плоский список без V2-полей")
    def test_v1_get_stays_flat_on_a_card_with_tree(self, created_card):
        card_id = created_card.id
        CardAttributesMergeV2API().merge_card_attributes_v2(card_id)

        response, model = CardAttributesListAPI().get_card_attributes(card_id)
        assert response.status_code == HTTPStatus.OK

        raw_items = response.json()
        assert len(raw_items) == 2, "v1 must show both tree nodes as a flat list"
        for raw_item in raw_items:
            assert "cardAttributeNodeID" not in raw_item
            assert "parentCardAttributeNodeID" not in raw_item
            assert "children" not in raw_item
        assert [item["sortOrder"] for item in raw_items] == [1, 2], (
            "v1 sortOrder must be sequential across the whole flat list"
        )

    @allure.title("Регрессия v1: PUT /cards/{id}/attributes не ломает parent-child связь дерева")
    def test_v1_merge_does_not_break_existing_tree(self, created_card):
        card_id = created_card.id
        CardAttributesMergeV2API().merge_card_attributes_v2(card_id)
        _, roots_before = CardAttributesListV2API().get_card_attributes_v2(card_id)
        assert len(roots_before[0].children) == 1

        # v1 merge adds a brand-new flat field — per AC it must land at root level
        # and must not touch the existing tree.
        CardAttributesMergeAPI().merge_card_attributes(card_id)

        _, roots_after = CardAttributesListV2API().get_card_attributes_v2(card_id)
        original_root = next(r for r in roots_after if r.cardAttributeNodeID == roots_before[0].cardAttributeNodeID)
        assert len(original_root.children) == 1, "v1 merge must not touch the pre-existing tree structure"

    @allure.title("V2 ручки без авторизации -> 401/403")
    @pytest.mark.ng
    def test_v2_without_auth_401(self, created_card):
        get_resp = CardAttributesListV2API().get_card_attributes_v2_without_auth(created_card.id)
        assert get_resp.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

        put_resp = CardAttributesMergeV2API().merge_card_attributes_v2_without_auth(created_card.id)
        assert put_resp.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

        delete_resp = CardAttributesDeleteV2API().delete_card_attribute_v2_without_auth(created_card.id, 1)
        assert delete_resp.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

    @allure.title("Узел не может быть сам себе родителем (self-reference в одном PUT) -> 409")
    @pytest.mark.ng
    def test_v2_self_parent_rejected(self, created_card):
        # First swap attempt (moving an existing root under its own existing child in one PUT)
        # turned out to be a *valid* restructuring — the whole subtree is redefined atomically,
        # so the backend can resolve it unambiguously (no real cycle, just a swap). A genuine
        # cycle only shows up when a node references its own cardAttributeNodeID twice in the
        # same request — confirmed live: 409 DuplicateCardAttributeNode.
        card_id = created_card.id
        create_resp, items = CardAttributesMergeV2API().merge_card_attributes_v2(
            card_id, payload=[Payloads.build_node(TEXT_ATTRIBUTE_ID, "Root")]
        )
        root_id = items[0].cardAttributeNodeID

        self_referencing_payload = [
            Payloads.build_node(
                TEXT_ATTRIBUTE_ID,
                "Root",
                card_attribute_node_id=root_id,
                children=[Payloads.build_node(TEXT_ATTRIBUTE_ID, "Root", card_attribute_node_id=root_id)],
            )
        ]
        response = CardAttributesMergeV2API().merge_card_attributes_v2_raw(card_id, self_referencing_payload)

        assert response.status_code == HTTPStatus.CONFLICT, (
            f"Expected HTTPStatus.CONFLICT (DuplicateCardAttributeNode), got {response.status_code}: {response.text}"
        )
