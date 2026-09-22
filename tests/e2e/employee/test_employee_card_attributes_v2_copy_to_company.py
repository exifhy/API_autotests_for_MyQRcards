from http import HTTPStatus

import allure
import pytest

from services.accounts.accounts_card_attributes_list_v2.api_accounts_card_attributes_list_v2 import (
    AccountsCardAttributesListV2API,
)
from services.accounts.accounts_card_attributes_merge_v2.api_accounts_card_attributes_merge_v2 import (
    AccountsCardAttributesMergeV2API,
)
from services.cards.card_attributes_merge_v2.payloads import Payloads
from src.resources.api import copy_cards_to_company
from testkit.fixtures.employee import _bulk_employee_flow, _safe_delete_invitation


def _node_signature(node) -> tuple:
    attribute = getattr(node, "attribute", None) or {}
    children = sorted(node.children or [], key=lambda c: c.sortOrder or 0)
    return (
        attribute.get("id"),
        node.sortOrder,
        tuple(node.values or []),
        tuple(_node_signature(child) for child in children),
    )


def _collect_node_ids(nodes) -> set[int]:
    ids: set[int] = set()
    for node in nodes:
        ids.add(node.cardAttributeNodeID)
        ids |= _collect_node_ids(node.children or [])
    return ids


def _assert_parent_links_correct(nodes, expected_parent_id=None) -> None:
    for node in nodes:
        assert node.parentCardAttributeNodeID == expected_parent_id, (
            f"Node {node.cardAttributeNodeID}: expected parentCardAttributeNodeID={expected_parent_id}, "
            f"got {node.parentCardAttributeNodeID}"
        )
        _assert_parent_links_correct(node.children or [], expected_parent_id=node.cardAttributeNodeID)


@allure.epic("LK")
@allure.feature("Employee")
@pytest.mark.e2e
@pytest.mark.employee
@allure.description(
    """
    REQUIREMENT 32324 — копирование визитки в компанию (POST /cards/card/copy) должно
    пересоздавать дерево дополнительных полей с новыми cardAttributeNodeID, сохраняя
    структуру parent-child, и не оставлять ссылок на узлы исходной визитки.
    """
)
class TestEmployeeCardAttributesV2CopyToCompany:
    @allure.title("Создать сотрудника → повесить дерево V2 → скопировать визитку в компанию → сверить дерево копии")
    def test_card_attributes_v2_tree_preserved_after_copy_to_company(self, lk_api, cfg):
        subscription_id = int(cfg["subscription_id"])
        source_company_id = int(cfg["company_id_create"])
        target_company_id = int(cfg["company_id_target"])

        flow = _bulk_employee_flow(
            lk_api,
            subscription_id=subscription_id,
            company_id=source_company_id,
            count=1,
            email_prefix="autotest_copytree",
            first_prefix="AT_CopyTreeFN",
            phone_prefix="8999333",
        )
        emp = flow["created"][0]
        account_id = emp["account_id"]
        invite_id = emp["invite_id"]
        card_id = emp["card_id"]
        assert card_id is not None, "Card id not resolved for created employee"

        try:
            with allure.step("01. PUT /Accounts/{account_id}/cards/{card_id}/attributes/V2 — attach a tree"):
                AccountsCardAttributesMergeV2API().merge_accounts_card_attributes_v2(
                    account_id,
                    card_id,
                    payload=Payloads.build_card_attributes_v2_payload(),
                )

            with allure.step("02. GET tree before copy"):
                before_nodes = AccountsCardAttributesListV2API().get_accounts_card_attributes_v2(
                    account_id, card_id
                )
                before_ids = _collect_node_ids(before_nodes)
                before_signature = sorted(
                    (_node_signature(n) for n in before_nodes), key=lambda s: s[1] or 0
                )
                assert before_ids, "Expected at least one attribute node before copy"

            with allure.step(f"03. POST /cards/card/copy — copy card to company {target_company_id}"):
                response = copy_cards_to_company(
                    lk_api,
                    [{"AccountID": account_id, "CardID": card_id, "CompanyID": target_company_id}],
                )
                assert response.status_code in (
                    HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT
                ), f"Card copy failed: {response.status_code} {response.text}"
                copy_result = response.json()
                new_card_id = next(
                    item["cardID"] for item in copy_result if int(item["accountID"]) == int(account_id)
                )
                assert int(new_card_id) != int(card_id), "Copy should get a different cardID from the source"

            with allure.step("04. GET tree of the copied card in target company"):
                after_nodes = AccountsCardAttributesListV2API().get_accounts_card_attributes_v2(
                    account_id, new_card_id
                )
                after_ids = _collect_node_ids(after_nodes)
                after_signature = sorted(
                    (_node_signature(n) for n in after_nodes), key=lambda s: s[1] or 0
                )

            with allure.step("05. Assert: new node ids, same structure, correct parent links"):
                assert after_ids, "Expected at least one attribute node after copy"
                assert after_ids.isdisjoint(before_ids), (
                    f"Copied tree must not reuse source node ids. "
                    f"before={sorted(before_ids)} after={sorted(after_ids)} "
                    f"overlap={sorted(after_ids & before_ids)}"
                )
                assert after_signature == before_signature, (
                    "Copied tree structure (attribute/sortOrder/values/children shape) must match the source"
                )
                _assert_parent_links_correct(after_nodes)

        finally:
            _safe_delete_invitation(lk_api, subscription_id, invite_id)
