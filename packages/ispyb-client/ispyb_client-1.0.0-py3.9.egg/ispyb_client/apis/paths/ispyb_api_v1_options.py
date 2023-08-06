from ispyb_client.paths.ispyb_api_v1_options.get import ApiForget
from ispyb_client.paths.ispyb_api_v1_options.patch import ApiForpatch


class IspybApiV1Options(
    ApiForget,
    ApiForpatch,
):
    pass
