# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from ispyb_client.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ADMIN = "Admin"
    AUTHENTICATION = "Authentication"
    CURRENT_USER = "Current User"
    DATA_COLLECTIONS = "Data Collections"
    DATA_COLLECTIONS__LEGACY_WITH_HEADER_TOKEN = "Data collections - legacy with header token"
    EM__LEGACY_WITH_HEADER_TOKEN = "EM - legacy with header token"
    EVENT_CHAINS = "Event chains"
    EVENTS = "Events"
    LAB_CONTACTS = "Lab Contacts"
    LEGACY_WITH_TOKEN_IN_PATH__ONLY_FOR_COMPATIBILITY_ = "Legacy with token in path ⚠️ only for compatibility ⚠️"
    OPTIONS = "Options"
    PROPOSALS = "Proposals"
    PROPOSALS__LEGACY_WITH_HEADER_TOKEN = "Proposals - legacy with header token"
    PROTEINS = "Proteins"
    SAMPLES = "Samples"
    SERIAL_CRYSTALLOGRAPHY = "Serial crystallography"
    SESSION = "Session"
    SESSIONS = "Sessions"
    SESSIONS__LEGACY_WITH_HEADER_TOKEN = "Sessions - legacy with header token"
    WEBSERVICES__SERIAL_CRYSTALLOGRAPHY = "Webservices - Serial crystallography"
    WEBSERVICES__USER_PORTAL_SYNC = "Webservices - User portal sync"
