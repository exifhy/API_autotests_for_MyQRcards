import allure
import pytest
from http import HTTPStatus

from services.attribute_type_groups.attribute_type_groups_list.api_attribute_type_groups_list import (
    AttributeTypeGroupsListAPI,
)


@allure.epic("API")
@allure.feature("AttributeTypeGroups")
@pytest.mark.api
@allure.description(
    """
    /AttributeTypeGroups
    """
)
class TestAttributeTypeGroupsList:
    @allure.title("GET /AttributeTypeGroups returns dictionary")
    @pytest.mark.smoke
    def test_attribute_type_groups_list_200_or_206(self):
        response, model = AttributeTypeGroupsListAPI().get_attribute_type_groups(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, dict)
        assert model.items, "Attribute type groups payload is empty"
        first_item = next(iter(model.items.values()))
        assert first_item.id is not None
        assert first_item.name is None or first_item.name != ""

    @allure.title("GET /AttributeTypeGroups supports offset/fetch query")
    def test_attribute_type_groups_list_with_paging_query(self):
        response, model = AttributeTypeGroupsListAPI().get_attribute_type_groups(
            range_header=None,
            offset=0,
            fetch=50,
        )

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, dict)

    @allure.title("GET /AttributeTypeGroups without auth")
    @pytest.mark.ng
    def test_attribute_type_groups_list_401_without_auth(self):
        response = AttributeTypeGroupsListAPI().get_attribute_type_groups_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
