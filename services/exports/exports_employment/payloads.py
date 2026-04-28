
class Payloads:
    @staticmethod
    def build_exports_employment_params(*, no_data: bool) -> dict:
        return {
            "noData": str(no_data).lower(),
        }
