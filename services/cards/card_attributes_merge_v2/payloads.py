from src.constants.attributes import PHONE_ATTRIBUTE_ID, TEXT_ATTRIBUTE_ID


class Payloads:
    @staticmethod
    def build_node(
        attribute_id: int,
        name: str,
        *,
        sort_order: int = 1,
        is_enabled: bool = True,
        value: list | None = None,
        children: list[dict] | None = None,
        card_attribute_node_id: int | None = None,
    ) -> dict:
        """Builds one node of the /attributes/V2 tree payload.

        Omit card_attribute_node_id (default) for a new node — the backend creates it.
        Pass an existing cardAttributeNodeID to update that node in place.
        """
        node = {
            "attributeID": attribute_id,
            "name": name,
            "sortOrder": sort_order,
            "isEnabled": is_enabled,
            "value": value if value is not None else [],
            "children": children if children is not None else [],
        }
        if card_attribute_node_id is not None:
            node["cardAttributeNodeID"] = card_attribute_node_id
        return node

    @staticmethod
    def build_card_attributes_v2_payload() -> list[dict]:
        """Default 2-level tree: a text "group" root with one phone child."""
        return [
            Payloads.build_node(
                TEXT_ATTRIBUTE_ID,
                "Group",
                children=[Payloads.build_node(PHONE_ATTRIBUTE_ID, "Phone", value=["+79000000001"])],
            )
        ]

    @staticmethod
    def build_nested_chain(depth: int, *, name_prefix: str = "L") -> list[dict]:
        """Builds a single root->child->grandchild->... chain `depth` levels deep
        (depth=1 is just a root, depth=3 is root->child->grandchild)."""
        node = Payloads.build_node(TEXT_ATTRIBUTE_ID, f"{name_prefix}{depth}")
        for level in range(depth - 1, 0, -1):
            node = Payloads.build_node(TEXT_ATTRIBUTE_ID, f"{name_prefix}{level}", children=[node])
        return [node]
