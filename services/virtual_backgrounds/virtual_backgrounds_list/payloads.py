
class Payloads:
    @staticmethod
    def build_virtual_backgrounds_query(*, offset: int | None = None, fetch: int | None = None) -> dict:
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)
        return params
