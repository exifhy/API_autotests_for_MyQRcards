import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    export_list_object_endpoint = f'{HOST}/EXPORT/assets'
    export_list_object_extended_endpoint = f'{HOST}/EXPORT/assets/extended'
    export_list_object_extended_includes_endpoint = f'{HOST}/EXPORT/assets/extended/includes'
    normal_export_list_object_endpoint = (f'{HOST}/EXPORT/assets?includePath=false&includeTaskActuality=true&'
                                          f'isDeleted=false&warrantyTill=9999-12-31T23%3')

    export_set_filters_endpoint = (f'{HOST}/EXPORT/assets/extended?include=ErpID&include=LocationAddress&include'
                                   f'=WorkTypeName&include=LocationLongitude&include=AssetClassName&include'
                                   f'=AssetContactFullName&include=AssetContactDescription&include=CompanyName'
                                   f'&include=IsMobileAsset&include=Name&include=Notes&include=LocationDescription'
                                   f'&include=ResponsiblePersonFullName&include=ParentAssetName&include=SerialNumber'
                                   f'&include=LocationCountryNameRu&include=AssetContactPhone&include=AssetTypeName'
                                   f'&include=DistrictName&include=LocationTimezoneNameRu&include=LocationLatitude'
                                   f'&include=AssetContactEmail&includePath=false&includeTaskActuality=true&isDeleted'
                                   f'=false&warrantyTill=9999-12-31T23%3A59%3A59')

    @staticmethod
    def export_all_filters_by_asset_id_endpoint(asset_id: int) -> str:
        endpoint = (f'{HOST}/EXPORT/assets/extended?assetID={asset_id}&include=ErpID&include=LocationAddress&include'
                    f'=WorkTypeName&include=LocationLongitude&include=AssetClassName&include'
                    f'=AssetContactFullName&include=AssetContactDescription&include=CompanyName'
                    f'&include=IsMobileAsset&include=Name&include=Notes&include=LocationDescription'
                    f'&include=ResponsiblePersonFullName&include=ParentAssetName&include=SerialNumber'
                    f'&include=LocationCountryNameRu&include=AssetContactPhone&include=AssetTypeName'
                    f'&include=DistrictName&include=LocationTimezoneNameRu&include=LocationLatitude'
                    f'&include=AssetContactEmail&includePath=false&includeTaskActuality=true&isDeleted'
                    f'=false&warrantyTill=9999-12-31T23%3A59%3A59')
        return endpoint

