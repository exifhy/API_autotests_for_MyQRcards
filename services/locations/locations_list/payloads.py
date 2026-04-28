
class Payloads:
    @staticmethod
    def build_locations_query(
        *,
        location_id: int | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ) -> dict:
        params: dict[str, str] = {}
        if location_id is not None:
            params["locationID"] = str(location_id)
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)
        return params
