import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_create.api_card_create import CardCreateAPI
from services.cards.card_leadgen_forms_create.api_card_leadgen_forms_create import (
    CardLeadGenFormsCreateAPI,
)
from services.contacts.contact_by_id.api_contact_by_id import ContactByIdAPI
from services.contacts.contact_create_web.api_contact_create_web import ContactCreateWebAPI
from services.contacts.contacts_list.api_contacts_list import ContactsListAPI
from services.leadgen.leadgen_form_fields.api_leadgen_form_fields import LeadGenFormFieldsAPI
from tests.api.cards.helpers import extract_card_link_id
from src.support.waiter import wait_until


@allure.epic("API")
@allure.feature("Contacts")
@pytest.mark.api
@pytest.mark.contacts
class TestContactsWebFlow:
    @allure.title("POST /accounts/contacts/web creates visible contact")
    def test_contact_create_web_flow(self, cfg, web_contact_ctx):
        created_card = CardCreateAPI().create_card(
            subscription_id=cfg["subscription_id"],
            company_id=cfg["company_id_create"],
        )
        assert created_card.id is not None
        web_contact_ctx["card_id"] = int(created_card.id)

        def _card_visible():
            try:
                return CardByIdAPI().get_card_by_id(created_card.id)
            except AssertionError:
                return None

        card = wait_until(_card_visible, timeout_s=30, step_s=2)
        assert card is not None, f"Created card {created_card.id} did not become visible"
        assert card.url, "Card public url is empty"

        _, field_templates = LeadGenFormFieldsAPI().get_leadgen_form_fields(offset=0, fetch=20)
        assert field_templates.items, "LeadGen form fields list is empty"
        field_template_id = next((item.id for item in field_templates.items if item.id is not None), None)
        assert field_template_id is not None, "No leadGen fieldTemplateID found"

        created_form = CardLeadGenFormsCreateAPI().create_card_leadgen_form(
            created_card.id,
            field_template_id=field_template_id,
        )
        assert created_form.id is not None
        web_contact_ctx["leadgen_form_id"] = int(created_form.id)

        payload = {
            "CardLinkID": extract_card_link_id(card.url),
            "LeadGenFormID": int(created_form.id),
            **web_contact_ctx["payload"],
        }

        response, model = ContactCreateWebAPI().create_contact(payload)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        if model.id is not None:
            web_contact_ctx["contact_id"] = int(model.id)

            def _created_by_id():
                try:
                    found = ContactByIdAPI().get_contact(model.id, app_id=web_contact_ctx["app_id"])
                except AssertionError:
                    return None
                return found if str(found.email or "").lower() == payload["Email"].lower() else None

            created = wait_until(_created_by_id, timeout_s=90, step_s=3)
        else:
            def _created_in_list():
                try:
                    _, items = ContactsListAPI().get_contacts(app_id=web_contact_ctx["app_id"])
                except AssertionError:
                    return None
                return next(
                    (
                        item
                        for item in items
                        if str(item.email or "").lower() == payload["Email"].lower()
                    ),
                    None,
                )

            created = wait_until(_created_in_list, timeout_s=90, step_s=3)
            if created and created.contactID is not None:
                web_contact_ctx["contact_id"] = int(created.contactID)

        assert created is not None, "Web-created contact did not appear in contacts APIs"
        assert str(created.email or "").lower() == payload["Email"].lower()
        assert str(created.firstName or "") == payload["FirstName"]
