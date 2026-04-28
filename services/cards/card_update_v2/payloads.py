from services.cards.card_update.payloads import Payloads as _CardUpdatePayloads


class Payloads:
    @staticmethod
    def build_card_update_v2_payload(*, company_id: int, gallery_attachment_ids: list[int] | None = None) -> dict:
        return _CardUpdatePayloads.build_card_update_payload(
            company_id=company_id,
            gallery_attachment_ids=gallery_attachment_ids,
        )
