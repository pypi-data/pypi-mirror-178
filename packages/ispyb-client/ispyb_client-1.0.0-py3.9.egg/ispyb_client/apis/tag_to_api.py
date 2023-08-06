import typing_extensions

from ispyb_client.apis.tags import TagValues
from ispyb_client.apis.tags.admin_api import AdminApi
from ispyb_client.apis.tags.authentication_api import AuthenticationApi
from ispyb_client.apis.tags.current_user_api import CurrentUserApi
from ispyb_client.apis.tags.data_collections_api import DataCollectionsApi
from ispyb_client.apis.tags.data_collections_legacy_with_header_token_api import DataCollectionsLegacyWithHeaderTokenApi
from ispyb_client.apis.tags.em_legacy_with_header_token_api import EMLegacyWithHeaderTokenApi
from ispyb_client.apis.tags.event_chains_api import EventChainsApi
from ispyb_client.apis.tags.events_api import EventsApi
from ispyb_client.apis.tags.lab_contacts_api import LabContactsApi
from ispyb_client.apis.tags.legacy_with_token_in_path_only_for_compatibility_api import LegacyWithTokenInPathOnlyForCompatibilityApi
from ispyb_client.apis.tags.options_api import OptionsApi
from ispyb_client.apis.tags.proposals_api import ProposalsApi
from ispyb_client.apis.tags.proposals_legacy_with_header_token_api import ProposalsLegacyWithHeaderTokenApi
from ispyb_client.apis.tags.proteins_api import ProteinsApi
from ispyb_client.apis.tags.samples_api import SamplesApi
from ispyb_client.apis.tags.serial_crystallography_api import SerialCrystallographyApi
from ispyb_client.apis.tags.session_api import SessionApi
from ispyb_client.apis.tags.sessions_api import SessionsApi
from ispyb_client.apis.tags.sessions_legacy_with_header_token_api import SessionsLegacyWithHeaderTokenApi
from ispyb_client.apis.tags.webservices_serial_crystallography_api import WebservicesSerialCrystallographyApi
from ispyb_client.apis.tags.webservices_user_portal_sync_api import WebservicesUserPortalSyncApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ADMIN: AdminApi,
        TagValues.AUTHENTICATION: AuthenticationApi,
        TagValues.CURRENT_USER: CurrentUserApi,
        TagValues.DATA_COLLECTIONS: DataCollectionsApi,
        TagValues.DATA_COLLECTIONS__LEGACY_WITH_HEADER_TOKEN: DataCollectionsLegacyWithHeaderTokenApi,
        TagValues.EM__LEGACY_WITH_HEADER_TOKEN: EMLegacyWithHeaderTokenApi,
        TagValues.EVENT_CHAINS: EventChainsApi,
        TagValues.EVENTS: EventsApi,
        TagValues.LAB_CONTACTS: LabContactsApi,
        TagValues.LEGACY_WITH_TOKEN_IN_PATH__ONLY_FOR_COMPATIBILITY_: LegacyWithTokenInPathOnlyForCompatibilityApi,
        TagValues.OPTIONS: OptionsApi,
        TagValues.PROPOSALS: ProposalsApi,
        TagValues.PROPOSALS__LEGACY_WITH_HEADER_TOKEN: ProposalsLegacyWithHeaderTokenApi,
        TagValues.PROTEINS: ProteinsApi,
        TagValues.SAMPLES: SamplesApi,
        TagValues.SERIAL_CRYSTALLOGRAPHY: SerialCrystallographyApi,
        TagValues.SESSION: SessionApi,
        TagValues.SESSIONS: SessionsApi,
        TagValues.SESSIONS__LEGACY_WITH_HEADER_TOKEN: SessionsLegacyWithHeaderTokenApi,
        TagValues.WEBSERVICES__SERIAL_CRYSTALLOGRAPHY: WebservicesSerialCrystallographyApi,
        TagValues.WEBSERVICES__USER_PORTAL_SYNC: WebservicesUserPortalSyncApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ADMIN: AdminApi,
        TagValues.AUTHENTICATION: AuthenticationApi,
        TagValues.CURRENT_USER: CurrentUserApi,
        TagValues.DATA_COLLECTIONS: DataCollectionsApi,
        TagValues.DATA_COLLECTIONS__LEGACY_WITH_HEADER_TOKEN: DataCollectionsLegacyWithHeaderTokenApi,
        TagValues.EM__LEGACY_WITH_HEADER_TOKEN: EMLegacyWithHeaderTokenApi,
        TagValues.EVENT_CHAINS: EventChainsApi,
        TagValues.EVENTS: EventsApi,
        TagValues.LAB_CONTACTS: LabContactsApi,
        TagValues.LEGACY_WITH_TOKEN_IN_PATH__ONLY_FOR_COMPATIBILITY_: LegacyWithTokenInPathOnlyForCompatibilityApi,
        TagValues.OPTIONS: OptionsApi,
        TagValues.PROPOSALS: ProposalsApi,
        TagValues.PROPOSALS__LEGACY_WITH_HEADER_TOKEN: ProposalsLegacyWithHeaderTokenApi,
        TagValues.PROTEINS: ProteinsApi,
        TagValues.SAMPLES: SamplesApi,
        TagValues.SERIAL_CRYSTALLOGRAPHY: SerialCrystallographyApi,
        TagValues.SESSION: SessionApi,
        TagValues.SESSIONS: SessionsApi,
        TagValues.SESSIONS__LEGACY_WITH_HEADER_TOKEN: SessionsLegacyWithHeaderTokenApi,
        TagValues.WEBSERVICES__SERIAL_CRYSTALLOGRAPHY: WebservicesSerialCrystallographyApi,
        TagValues.WEBSERVICES__USER_PORTAL_SYNC: WebservicesUserPortalSyncApi,
    }
)
