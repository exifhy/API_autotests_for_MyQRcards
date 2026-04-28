
class Payloads:
    """Query builders for GET /Companies."""


    @staticmethod
    def build_companies_query(
        *,
        search_text: str | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ) -> dict:
        params: dict[str, str] = {}
        if search_text:
            params["searchText"] = search_text
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)
        return params
