from src.utils.randoms import rand_email, rand_word


class Payloads:
    @staticmethod
    def build_company_update_payload() -> dict:
        suf = rand_word("upd", 10).replace("upd_", "")
        return {
            "Name": f"AT_UpdatedCompany_{suf}",
            "Phone": "+78120000000",
            "Fax": "+78121111111",
            "Email": rand_email(domain="tt.tt"),
            "SiteUrl": "https://www.updated-test.tt",
            "FoundedYear": 2024,
            "Activity": "Updated activity",
            "Customers": "Updated customers",
            "LogoAttachmentID": None,
            "Location": {
                "Country": "Russia",
                "PostalCode": "190000",
                "Region": "Saint Petersburg",
                "City": "Saint Petersburg",
                "Address": "Nevsky prospect, 1",
                "Notes": "updated office",
                "Latitude": 59.9343,
                "Longitude": 30.3351,
            },
            "SocialNetworks": [
                {"SocialNetworkID": 1, "ContactUrl": "https://vk.com/updated_test"},
                {"SocialNetworkID": 7, "ContactUrl": "tg://resolve?domain=updatedtest"},
            ],
        }
