from src.utils.randoms import rand_email, rand_word


class Payloads:
    @staticmethod
    def build_company_create_payload(*, logo_id: int | None = None) -> dict:
        payload = {
            "Name": rand_word("Api_tests_company", 8),
            "Phone": "+78129875643",
            "Fax": "+78129875643",
            "Email": rand_email(domain="tt.tt"),
            "SiteUrl": "https://www.test.tt",
            "FoundedYear": 2018,
            "Activity": "Testing, Testing, Testing",
            "Customers": "Testers, Testers",
            "Location": {
                "Country": "Russia",
                "PostalCode": "198198",
                "Region": "Leningradskaya oblast",
                "Address": "Murino, Shuvalova 9",
                "Notes": "13 app.",
                "Latitude": "32.987656",
                "Longitude": "32.987656",
            },
            "SocialNetworks": [
                {"SocialNetworkID": 1, "ContactUrl": "https://cn.com/test"},
                {"SocialNetworkID": 7, "ContactUrl": "tg://resolve?domain=zdarova"},
                {"SocialNetworkID": 8, "ContactUrl": "https://wa.me/+89452342323"},
                {"SocialNetworkID": 9, "ContactUrl": "viber://chat?number=86767575676"},
                {"SocialNetworkID": 19, "ContactUrl": "86767575676"},
            ],
        }
        if logo_id is not None:
            payload["logoAttachmentID"] = int(logo_id)
        return payload
