
class Payloads:
    @staticmethod
    def build_attribute_type_groups_params(*, offset: int | None = None, fetch: int | None = None) -> dict[str, str] | None:
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)
        return params or None
