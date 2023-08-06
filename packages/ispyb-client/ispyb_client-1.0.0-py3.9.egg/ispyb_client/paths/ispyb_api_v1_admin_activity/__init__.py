# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from ispyb_client.paths.ispyb_api_v1_admin_activity import Api

from ispyb_client.paths import PathValues

path = PathValues.ISPYB_API_V1_ADMIN_ACTIVITY