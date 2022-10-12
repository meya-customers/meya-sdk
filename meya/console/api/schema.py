import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay

schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
schema -= sgqlc.types.relay.Node
schema -= sgqlc.types.relay.PageInfo


########################################################################
# Scalars and Enumerations
########################################################################
class AppStateEnum(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "DELETED",
        "DEPLOYING",
        "ERROR",
        "RUNNING",
        "STARTING",
        "STOPPED",
    )


class AppTypeEnum(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("DEV", "STAGING", "PRODUCTION")


Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int


class InviteState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("CREATED", "PENDING", "RESENT", "REVOKED")


class JSONString(sgqlc.types.Scalar):
    __schema__ = schema


class Money(sgqlc.types.Scalar):
    __schema__ = schema


class PushAppType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("DEV", "STAGING", "PRODUCTION")


class PushPushType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("IMAGE_BUILD", "RELOAD")


class PushState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "BUILDING",
        "CANCELLED",
        "COMPLETE",
        "DEPLOYING",
        "FAILED",
        "QUEUED",
        "RUNNING",
    )


String = sgqlc.types.String


class UserFlowEditorMode(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("NONE", "VISUAL", "CODE")


class UserVisualScrollMode(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("NONE", "MOUSE", "TRACKPAD")


########################################################################
# Input Objects
########################################################################
class AccountLimitsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("dev_apps", "staging_apps", "production_apps")
    dev_apps = sgqlc.types.Field(Int, graphql_name="devApps")
    staging_apps = sgqlc.types.Field(Int, graphql_name="stagingApps")
    production_apps = sgqlc.types.Field(Int, graphql_name="productionApps")


########################################################################
# Output Objects and Interfaces
########################################################################
class AccountMetaType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "total_dev_apps",
        "total_staging_apps",
        "total_production_apps",
        "total_team_members",
        "total_teams",
        "total_invites",
    )
    total_dev_apps = sgqlc.types.Field(Int, graphql_name="totalDevApps")
    total_staging_apps = sgqlc.types.Field(
        Int, graphql_name="totalStagingApps"
    )
    total_production_apps = sgqlc.types.Field(
        Int, graphql_name="totalProductionApps"
    )
    total_team_members = sgqlc.types.Field(
        Int, graphql_name="totalTeamMembers"
    )
    total_teams = sgqlc.types.Field(Int, graphql_name="totalTeams")
    total_invites = sgqlc.types.Field(Int, graphql_name="totalInvites")


class AccountType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "name",
        "enabled",
        "meta",
        "users",
        "invites",
        "apps",
        "teams",
        "team_permissions",
        "permissions",
        "limits",
        "usage",
        "next_billing_date",
        "metering_offset_hours",
        "subscription",
        "usage_subscription",
        "components",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="enabled"
    )
    meta = sgqlc.types.Field(AccountMetaType, graphql_name="meta")
    users = sgqlc.types.Field(
        sgqlc.types.list_of("UserType"),
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "email",
                    sgqlc.types.Arg(
                        String, graphql_name="email", default=None
                    ),
                ),
                (
                    "email__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="email_Icontains", default=None
                    ),
                ),
                (
                    "email__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="email_Istartswith", default=None
                    ),
                ),
                (
                    "full_name",
                    sgqlc.types.Arg(
                        String, graphql_name="fullName", default=None
                    ),
                ),
                (
                    "full_name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="fullName_Icontains", default=None
                    ),
                ),
                (
                    "full_name__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="fullName_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    invites = sgqlc.types.Field(
        sgqlc.types.list_of("InviteType"),
        graphql_name="invites",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "team__id",
                    sgqlc.types.Arg(ID, graphql_name="team_Id", default=None),
                ),
                (
                    "team__name",
                    sgqlc.types.Arg(
                        String, graphql_name="team_Name", default=None
                    ),
                ),
                (
                    "team__name__icontains",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="team_Name_Icontains",
                        default=None,
                    ),
                ),
                (
                    "team__name__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="team_Name_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "team__account__id",
                    sgqlc.types.Arg(
                        ID, graphql_name="team_Account_Id", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    apps = sgqlc.types.Field(
        sgqlc.types.list_of("AppType"),
        graphql_name="apps",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    teams = sgqlc.types.Field(
        sgqlc.types.list_of("TeamType"),
        graphql_name="teams",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "account__id",
                    sgqlc.types.Arg(
                        ID, graphql_name="account_Id", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    team_permissions = sgqlc.types.Field(
        sgqlc.types.list_of("PermissionSetType"),
        graphql_name="teamPermissions",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    permissions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="permissions"
    )
    limits = sgqlc.types.Field(JSONString, graphql_name="limits")
    usage = sgqlc.types.Field("AccountUsageType", graphql_name="usage")
    next_billing_date = sgqlc.types.Field(
        DateTime, graphql_name="nextBillingDate"
    )
    metering_offset_hours = sgqlc.types.Field(
        Int, graphql_name="meteringOffsetHours"
    )
    subscription = sgqlc.types.Field(
        "SubscriptionType", graphql_name="subscription"
    )
    usage_subscription = sgqlc.types.Field(
        "SubscriptionType", graphql_name="usageSubscription"
    )
    components = sgqlc.types.Field(
        sgqlc.types.list_of("ComponentType"),
        graphql_name="components",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_type",
                    sgqlc.types.Arg(
                        AppTypeEnum, graphql_name="appType", default=None
                    ),
                ),
            )
        ),
    )


class AccountUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("account",)
    account = sgqlc.types.Field(AccountType, graphql_name="account")


class AccountUsageType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("users", "events")
    users = sgqlc.types.Field(JSONString, graphql_name="users")
    events = sgqlc.types.Field(JSONString, graphql_name="events")


class AppAnalyticsType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("total_users", "total_events", "events", "users")
    total_users = sgqlc.types.Field(Int, graphql_name="totalUsers")
    total_events = sgqlc.types.Field(Int, graphql_name="totalEvents")
    events = sgqlc.types.Field(JSONString, graphql_name="events")
    users = sgqlc.types.Field(JSONString, graphql_name="users")


class AppCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app", "next_revision")
    app = sgqlc.types.Field("AppType", graphql_name="app")
    next_revision = sgqlc.types.Field(String, graphql_name="nextRevision")


class AppDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app",)
    app = sgqlc.types.Field("AppType", graphql_name="app")


class AppEntryType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "entry_id",
        "trace_id",
        "app_id",
        "entry_timestamp",
        "entry_sequence",
        "type",
        "data",
    )
    id = sgqlc.types.Field(ID, graphql_name="id")
    entry_id = sgqlc.types.Field(String, graphql_name="entryId")
    trace_id = sgqlc.types.Field(String, graphql_name="traceId")
    app_id = sgqlc.types.Field(String, graphql_name="appId")
    entry_timestamp = sgqlc.types.Field(
        DateTime, graphql_name="entryTimestamp"
    )
    entry_sequence = sgqlc.types.Field(Int, graphql_name="entrySequence")
    type = sgqlc.types.Field(String, graphql_name="type")
    data = sgqlc.types.Field(JSONString, graphql_name="data")


class AppPushMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("push", "result")
    push = sgqlc.types.Field("PushType", graphql_name="push")
    result = sgqlc.types.Field(String, graphql_name="result")


class AppStartMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app",)
    app = sgqlc.types.Field("AppType", graphql_name="app")


class AppStopMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app",)
    app = sgqlc.types.Field("AppType", graphql_name="app")


class AppTeamCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app", "team", "app_team")
    app = sgqlc.types.Field("AppType", graphql_name="app")
    team = sgqlc.types.Field("TeamType", graphql_name="team")
    app_team = sgqlc.types.Field("AppTeamType", graphql_name="appTeam")


class AppTeamDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app_team",)
    app_team = sgqlc.types.Field("AppTeamType", graphql_name="appTeam")


class AppTeamType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "app", "permission_set", "team")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    app = sgqlc.types.Field("AppType", graphql_name="app")
    permission_set = sgqlc.types.Field(
        "PermissionSetType", graphql_name="permissionSet"
    )
    team = sgqlc.types.Field("TeamType", graphql_name="team")


class AppTeamUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app_team",)
    app_team = sgqlc.types.Field(AppTeamType, graphql_name="appTeam")


class AppTryDecryptSensitiveMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("result",)
    result = sgqlc.types.Field(
        sgqlc.types.list_of(JSONString), graphql_name="result"
    )


class AppType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "name",
        "app_type",
        "state",
        "state_message",
        "account",
        "app_teams",
        "permissions",
        "logs",
        "users",
        "analytics",
        "vault",
        "internal_vault",
        "pushes",
        "last_push",
        "grid_version",
        "editor_schemas",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    app_type = sgqlc.types.Field(AppTypeEnum, graphql_name="appType")
    state = sgqlc.types.Field(AppStateEnum, graphql_name="state")
    state_message = sgqlc.types.Field(String, graphql_name="stateMessage")
    account = sgqlc.types.Field(AccountType, graphql_name="account")
    app_teams = sgqlc.types.Field(
        sgqlc.types.list_of(AppTeamType),
        graphql_name="appTeams",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "app__id",
                    sgqlc.types.Arg(ID, graphql_name="app_Id", default=None),
                ),
                (
                    "team__id",
                    sgqlc.types.Arg(ID, graphql_name="team_Id", default=None),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    permissions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="permissions"
    )
    logs = sgqlc.types.Field(
        "LogType",
        graphql_name="logs",
        args=sgqlc.types.ArgDict(
            (
                (
                    "query",
                    sgqlc.types.Arg(
                        String, graphql_name="query", default=None
                    ),
                ),
                (
                    "limit",
                    sgqlc.types.Arg(Int, graphql_name="limit", default=None),
                ),
                (
                    "previous_oldest_timestamp",
                    sgqlc.types.Arg(
                        DateTime,
                        graphql_name="previousOldestTimestamp",
                        default=None,
                    ),
                ),
                (
                    "previous_oldest_sequence",
                    sgqlc.types.Arg(
                        Int,
                        graphql_name="previousOldestSequence",
                        default=None,
                    ),
                ),
                (
                    "previous_oldest_type",
                    sgqlc.types.Arg(
                        String, graphql_name="previousOldestType", default=None
                    ),
                ),
                (
                    "previous_oldest_id",
                    sgqlc.types.Arg(
                        Int, graphql_name="previousOldestId", default=None
                    ),
                ),
                (
                    "offset",
                    sgqlc.types.Arg(Int, graphql_name="offset", default=None),
                ),
            )
        ),
    )
    users = sgqlc.types.Field(
        "AppUserTypeConnection",
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (
                (
                    "before",
                    sgqlc.types.Arg(
                        String, graphql_name="before", default=None
                    ),
                ),
                (
                    "after",
                    sgqlc.types.Arg(
                        String, graphql_name="after", default=None
                    ),
                ),
                (
                    "first",
                    sgqlc.types.Arg(Int, graphql_name="first", default=None),
                ),
                (
                    "last",
                    sgqlc.types.Arg(Int, graphql_name="last", default=None),
                ),
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "id__lt",
                    sgqlc.types.Arg(ID, graphql_name="id_Lt", default=None),
                ),
                (
                    "id__lte",
                    sgqlc.types.Arg(ID, graphql_name="id_Lte", default=None),
                ),
                (
                    "id__gt",
                    sgqlc.types.Arg(ID, graphql_name="id_Gt", default=None),
                ),
                (
                    "id__gte",
                    sgqlc.types.Arg(ID, graphql_name="id_Gte", default=None),
                ),
                (
                    "created",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="created", default=None
                    ),
                ),
                (
                    "created__lt",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="created_Lt", default=None
                    ),
                ),
                (
                    "created__lte",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="created_Lte", default=None
                    ),
                ),
                (
                    "created__gt",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="created_Gt", default=None
                    ),
                ),
                (
                    "created__gte",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="created_Gte", default=None
                    ),
                ),
                (
                    "modified",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="modified", default=None
                    ),
                ),
                (
                    "modified__lt",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="modified_Lt", default=None
                    ),
                ),
                (
                    "modified__lte",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="modified_Lte", default=None
                    ),
                ),
                (
                    "modified__gt",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="modified_Gt", default=None
                    ),
                ),
                (
                    "modified__gte",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="modified_Gte", default=None
                    ),
                ),
                (
                    "name_icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="nameIcontains", default=None
                    ),
                ),
                (
                    "email_icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="emailIcontains", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    analytics = sgqlc.types.Field(
        AppAnalyticsType,
        graphql_name="analytics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "from_date",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DateTime),
                        graphql_name="fromDate",
                        default=None,
                    ),
                ),
                (
                    "to_date",
                    sgqlc.types.Arg(
                        DateTime, graphql_name="toDate", default=None
                    ),
                ),
            )
        ),
    )
    vault = sgqlc.types.Field("SecretType", graphql_name="vault")
    internal_vault = sgqlc.types.Field(
        "SecretType", graphql_name="internalVault"
    )
    pushes = sgqlc.types.Field(
        sgqlc.types.list_of("PushType"),
        graphql_name="pushes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "offset",
                    sgqlc.types.Arg(Int, graphql_name="offset", default=None),
                ),
                (
                    "limit",
                    sgqlc.types.Arg(Int, graphql_name="limit", default=None),
                ),
            )
        ),
    )
    last_push = sgqlc.types.Field("PushType", graphql_name="lastPush")
    grid_version = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="gridVersion"
    )
    editor_schemas = sgqlc.types.Field(
        JSONString, graphql_name="editorSchemas"
    )


class AppUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("app",)
    app = sgqlc.types.Field(AppType, graphql_name="app")


class AppUpdateVaultMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("vault",)
    vault = sgqlc.types.Field(JSONString, graphql_name="vault")


class AppUserTypeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(
        sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo"
    )
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("AppUserTypeEdge")),
        graphql_name="edges",
    )


class AppUserTypeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("node", "cursor")
    node = sgqlc.types.Field("AppUserType", graphql_name="node")
    cursor = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="cursor"
    )


class CancelPushMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("push",)
    push = sgqlc.types.Field("PushType", graphql_name="push")


class ClusterType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name", "grid_url", "description", "config")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    grid_url = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="gridUrl"
    )
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )
    config = sgqlc.types.Field(JSONString, graphql_name="config")


class ComponentType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name", "limits", "default_unit_price")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    limits = sgqlc.types.Field(JSONString, graphql_name="limits")
    default_unit_price = sgqlc.types.Field(
        "MoneyType", graphql_name="defaultUnitPrice"
    )


class ConsolePushMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("result",)
    result = sgqlc.types.Field(String, graphql_name="result")


class GatewayPushMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("result",)
    result = sgqlc.types.Field(String, graphql_name="result")


class InviteCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("invite",)
    invite = sgqlc.types.Field("InviteType", graphql_name="invite")


class InviteResendMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("invite",)
    invite = sgqlc.types.Field("InviteType", graphql_name="invite")


class InviteRevokeMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("invite_id",)
    invite_id = sgqlc.types.Field(ID, graphql_name="inviteId")


class InviteType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "email",
        "state",
        "team",
        "valid",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    state = sgqlc.types.Field(
        sgqlc.types.non_null(InviteState), graphql_name="state"
    )
    team = sgqlc.types.Field("TeamType", graphql_name="team")
    valid = sgqlc.types.Field(Boolean, graphql_name="valid")


class LogType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "query_id",
        "complete",
        "newest_timestamp",
        "oldest_timestamp",
        "oldest_sequence",
        "oldest_type",
        "oldest_id",
        "entries",
    )
    query_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="queryId"
    )
    complete = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="complete"
    )
    newest_timestamp = sgqlc.types.Field(
        DateTime, graphql_name="newestTimestamp"
    )
    oldest_timestamp = sgqlc.types.Field(
        DateTime, graphql_name="oldestTimestamp"
    )
    oldest_sequence = sgqlc.types.Field(Int, graphql_name="oldestSequence")
    oldest_type = sgqlc.types.Field(String, graphql_name="oldestType")
    oldest_id = sgqlc.types.Field(Int, graphql_name="oldestId")
    entries = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(AppEntryType)),
        graphql_name="entries",
    )


class MeyaOAuthDeleteSubscriptionMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(Boolean, graphql_name="ok")


class MeyaOAuthMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("step", "authorization_url")
    step = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="step")
    authorization_url = sgqlc.types.Field(
        String, graphql_name="authorizationUrl"
    )


class MoneyType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("amount", "currency", "formatted_amount")
    amount = sgqlc.types.Field(Float, graphql_name="amount")
    currency = sgqlc.types.Field(String, graphql_name="currency")
    formatted_amount = sgqlc.types.Field(Money, graphql_name="formattedAmount")


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "update_user",
        "update_user_flow_editor_mode",
        "update_user_visual_scroll_mode",
        "update_user_editor_advanced_mode",
        "update_user_editor_simulator_opened",
        "refresh_user_auth_token",
        "update_account",
        "create_app",
        "update_app",
        "delete_app",
        "update_app_vault",
        "push_app",
        "start_app",
        "stop_app",
        "try_decrypt_sensitive_app_data",
        "update_team",
        "create_team",
        "delete_team",
        "add_team_member",
        "remove_team_member",
        "remove_user",
        "create_invite",
        "resend_invite",
        "revoke_invite",
        "update_app_team",
        "create_app_team",
        "delete_app_team",
        "push_console",
        "push_gateway",
        "cancel_push",
        "meya_oauth",
        "meya_oauth_delete_subscription",
        "twitter_get_webhook_ids",
        "twitter_registry_webhook",
        "twitter_delete_webhook_registry",
        "twitter_list_subscriptions",
        "twitter_create_welcome_message",
        "twitter_list_welcome_message",
        "twitter_delete_welcome_message",
        "twitter_create_welcome_message_rule",
        "twitter_delete_welcome_message_rule",
        "twitter_list_welcome_message_rule",
    )
    update_user = sgqlc.types.Field(
        "UserUpdateMutation",
        graphql_name="updateUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "full_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="fullName",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "visual_scroll_mode",
                    sgqlc.types.Arg(
                        String, graphql_name="visualScrollMode", default=None
                    ),
                ),
            )
        ),
    )
    update_user_flow_editor_mode = sgqlc.types.Field(
        "UserUpdateFlowEditorModeMutation",
        graphql_name="updateUserFlowEditorMode",
        args=sgqlc.types.ArgDict(
            (
                (
                    "flow_editor_mode",
                    sgqlc.types.Arg(
                        String, graphql_name="flowEditorMode", default=None
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_user_visual_scroll_mode = sgqlc.types.Field(
        "UserUpdateVisualScrollModeMutation",
        graphql_name="updateUserVisualScrollMode",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "visual_scroll_mode",
                    sgqlc.types.Arg(
                        String, graphql_name="visualScrollMode", default=None
                    ),
                ),
            )
        ),
    )
    update_user_editor_advanced_mode = sgqlc.types.Field(
        "UserUpdateEditorAdvancedModeMutation",
        graphql_name="updateUserEditorAdvancedMode",
        args=sgqlc.types.ArgDict(
            (
                (
                    "editor_advanced_mode",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="editorAdvancedMode",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_user_editor_simulator_opened = sgqlc.types.Field(
        "UserUpdateEditorSimulatorOpenedMutation",
        graphql_name="updateUserEditorSimulatorOpened",
        args=sgqlc.types.ArgDict(
            (
                (
                    "editor_simulator_opened",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="editorSimulatorOpened",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    refresh_user_auth_token = sgqlc.types.Field(
        "UserRefreshAuthTokenMutation",
        graphql_name="refreshUserAuthToken",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_account = sgqlc.types.Field(
        AccountUpdateMutation,
        graphql_name="updateAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "limits",
                    sgqlc.types.Arg(
                        AccountLimitsInput, graphql_name="limits", default=None
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
            )
        ),
    )
    create_app = sgqlc.types.Field(
        AppCreateMutation,
        graphql_name="createApp",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "app_type",
                    sgqlc.types.Arg(
                        AppTypeEnum, graphql_name="appType", default=None
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="name",
                        default=None,
                    ),
                ),
                (
                    "template_repo_url",
                    sgqlc.types.Arg(
                        String, graphql_name="templateRepoUrl", default=None
                    ),
                ),
            )
        ),
    )
    update_app = sgqlc.types.Field(
        AppUpdateMutation,
        graphql_name="updateApp",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_type",
                    sgqlc.types.Arg(
                        AppTypeEnum, graphql_name="appType", default=None
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
            )
        ),
    )
    delete_app = sgqlc.types.Field(
        AppDeleteMutation,
        graphql_name="deleteApp",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_app_vault = sgqlc.types.Field(
        AppUpdateVaultMutation,
        graphql_name="updateAppVault",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "vault",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSONString),
                        graphql_name="vault",
                        default=None,
                    ),
                ),
            )
        ),
    )
    push_app = sgqlc.types.Field(
        AppPushMutation,
        graphql_name="pushApp",
        args=sgqlc.types.ArgDict(
            (
                (
                    "build_image",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="buildImage", default=None
                    ),
                ),
                (
                    "grid",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="grid", default=None
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "next_revision",
                    sgqlc.types.Arg(
                        String, graphql_name="nextRevision", default=None
                    ),
                ),
            )
        ),
    )
    start_app = sgqlc.types.Field(
        AppStartMutation,
        graphql_name="startApp",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "increase_limit",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="increaseLimit", default=None
                    ),
                ),
            )
        ),
    )
    stop_app = sgqlc.types.Field(
        AppStopMutation,
        graphql_name="stopApp",
        args=sgqlc.types.ArgDict(
            (
                (
                    "decrease_limit",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="decreaseLimit", default=None
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    try_decrypt_sensitive_app_data = sgqlc.types.Field(
        AppTryDecryptSensitiveMutation,
        graphql_name="tryDecryptSensitiveAppData",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "sensitive_data_refs",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(String)),
                        graphql_name="sensitiveDataRefs",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_team = sgqlc.types.Field(
        "TeamUpdateMutation",
        graphql_name="updateTeam",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "permission_set_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="permissionSetId", default=None
                    ),
                ),
            )
        ),
    )
    create_team = sgqlc.types.Field(
        "TeamCreateMutation",
        graphql_name="createTeam",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "permission_set_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="permissionSetId", default=None
                    ),
                ),
            )
        ),
    )
    delete_team = sgqlc.types.Field(
        "TeamDeleteMutation",
        graphql_name="deleteTeam",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    add_team_member = sgqlc.types.Field(
        "TeamMemberAddMutation",
        graphql_name="addTeamMember",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "team_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="teamId",
                        default=None,
                    ),
                ),
                (
                    "user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="userId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    remove_team_member = sgqlc.types.Field(
        "TeamMemberRemoveMutation",
        graphql_name="removeTeamMember",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    remove_user = sgqlc.types.Field(
        "TeamMemberRemoveAllMutation",
        graphql_name="removeUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="userId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_invite = sgqlc.types.Field(
        InviteCreateMutation,
        graphql_name="createInvite",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="email",
                        default=None,
                    ),
                ),
                (
                    "team_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="teamId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    resend_invite = sgqlc.types.Field(
        InviteResendMutation,
        graphql_name="resendInvite",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "invite_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="inviteId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    revoke_invite = sgqlc.types.Field(
        InviteRevokeMutation,
        graphql_name="revokeInvite",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "invite_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="inviteId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_app_team = sgqlc.types.Field(
        AppTeamUpdateMutation,
        graphql_name="updateAppTeam",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "permission_set_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="permissionSetId", default=None
                    ),
                ),
            )
        ),
    )
    create_app_team = sgqlc.types.Field(
        AppTeamCreateMutation,
        graphql_name="createAppTeam",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "permission_set_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="permissionSetId", default=None
                    ),
                ),
                (
                    "team_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="teamId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_app_team = sgqlc.types.Field(
        AppTeamDeleteMutation,
        graphql_name="deleteAppTeam",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    push_console = sgqlc.types.Field(
        ConsolePushMutation,
        graphql_name="pushConsole",
        args=sgqlc.types.ArgDict(
            (
                (
                    "build_image",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="buildImage", default=None
                    ),
                ),
                (
                    "install",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="install", default=None
                    ),
                ),
                (
                    "migrate",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="migrate", default=None
                    ),
                ),
                (
                    "migrate_app_label",
                    sgqlc.types.Arg(
                        String, graphql_name="migrateAppLabel", default=None
                    ),
                ),
                (
                    "migrate_database",
                    sgqlc.types.Arg(
                        String, graphql_name="migrateDatabase", default=None
                    ),
                ),
                (
                    "migrate_migration_name",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="migrateMigrationName",
                        default=None,
                    ),
                ),
                (
                    "next_revision",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="nextRevision",
                        default=None,
                    ),
                ),
            )
        ),
    )
    push_gateway = sgqlc.types.Field(
        GatewayPushMutation,
        graphql_name="pushGateway",
        args=sgqlc.types.ArgDict(
            (
                (
                    "next_revision",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="nextRevision",
                        default=None,
                    ),
                ),
            )
        ),
    )
    cancel_push = sgqlc.types.Field(
        CancelPushMutation,
        graphql_name="cancelPush",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    meya_oauth = sgqlc.types.Field(
        MeyaOAuthMutation,
        graphql_name="meyaOauth",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "element_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="elementType",
                        default=None,
                    ),
                ),
                (
                    "integration_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="integrationId",
                        default=None,
                    ),
                ),
                (
                    "integration_path",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="integrationPath",
                        default=None,
                    ),
                ),
                (
                    "response_request",
                    sgqlc.types.Arg(
                        String, graphql_name="responseRequest", default=""
                    ),
                ),
            )
        ),
    )
    meya_oauth_delete_subscription = sgqlc.types.Field(
        MeyaOAuthDeleteSubscriptionMutation,
        graphql_name="meyaOauthDeleteSubscription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "element_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="elementType",
                        default=None,
                    ),
                ),
                (
                    "integration_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="integrationId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_get_webhook_ids = sgqlc.types.Field(
        "TwitterListWebhooksMutation", graphql_name="twitterGetWebhookIds"
    )
    twitter_registry_webhook = sgqlc.types.Field(
        "TwitterRegistryWebhookMutation",
        graphql_name="twitterRegistryWebhook",
        args=sgqlc.types.ArgDict(
            (
                (
                    "webhook_uri",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="webhookUri",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_delete_webhook_registry = sgqlc.types.Field(
        "TwitterDeleteWebhookRegistryMutation",
        graphql_name="twitterDeleteWebhookRegistry",
        args=sgqlc.types.ArgDict(
            (
                (
                    "webhook_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="webhookId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_list_subscriptions = sgqlc.types.Field(
        "TwitterListSubscriptionsMutation",
        graphql_name="twitterListSubscriptions",
    )
    twitter_create_welcome_message = sgqlc.types.Field(
        "TwitterCreateWelcomeMessageMutation",
        graphql_name="twitterCreateWelcomeMessage",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "welcome_message",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSONString),
                        graphql_name="welcomeMessage",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_list_welcome_message = sgqlc.types.Field(
        "TwitterListWelcomeMessageMutation",
        graphql_name="twitterListWelcomeMessage",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "count",
                    sgqlc.types.Arg(Int, graphql_name="count", default=0),
                ),
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=""),
                ),
            )
        ),
    )
    twitter_delete_welcome_message = sgqlc.types.Field(
        "TwitterDeleteWelcomeMessageMutation",
        graphql_name="twitterDeleteWelcomeMessage",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "welcome_message_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="welcomeMessageId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_create_welcome_message_rule = sgqlc.types.Field(
        "TwitterCreateWelcomeMessageRuleMutation",
        graphql_name="twitterCreateWelcomeMessageRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "welcome_message_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="welcomeMessageId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_delete_welcome_message_rule = sgqlc.types.Field(
        "TwitterDeleteWelcomeMessageRuleMutation",
        graphql_name="twitterDeleteWelcomeMessageRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "welcome_message_rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="welcomeMessageRuleId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    twitter_list_welcome_message_rule = sgqlc.types.Field(
        "TwitterListWelcomeMessageRuleMutation",
        graphql_name="twitterListWelcomeMessageRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="appId",
                        default=None,
                    ),
                ),
                (
                    "count",
                    sgqlc.types.Arg(Int, graphql_name="count", default=0),
                ),
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=""),
                ),
            )
        ),
    )


class Node(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class PageInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "has_next_page",
        "has_previous_page",
        "start_cursor",
        "end_cursor",
    )
    has_next_page = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasNextPage"
    )
    has_previous_page = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasPreviousPage"
    )
    start_cursor = sgqlc.types.Field(String, graphql_name="startCursor")
    end_cursor = sgqlc.types.Field(String, graphql_name="endCursor")


class PermissionSetType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name", "description", "internal")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )
    internal = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="internal"
    )


class ProductType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name", "limits")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    limits = sgqlc.types.Field(JSONString, graphql_name="limits")


class PushType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "app",
        "app_type",
        "push_type",
        "next_revision",
        "state",
        "state_message",
        "user",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    app = sgqlc.types.Field(sgqlc.types.non_null(AppType), graphql_name="app")
    app_type = sgqlc.types.Field(PushAppType, graphql_name="appType")
    push_type = sgqlc.types.Field(PushPushType, graphql_name="pushType")
    next_revision = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="nextRevision"
    )
    state = sgqlc.types.Field(PushState, graphql_name="state")
    state_message = sgqlc.types.Field(String, graphql_name="stateMessage")
    user = sgqlc.types.Field("UserType", graphql_name="user")


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "user",
        "clusters",
        "cdn_url",
        "versions",
        "all_apps",
        "active_apps",
    )
    user = sgqlc.types.Field("UserType", graphql_name="user")
    clusters = sgqlc.types.Field(
        sgqlc.types.list_of(ClusterType),
        graphql_name="clusters",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "grid_url",
                    sgqlc.types.Arg(
                        String, graphql_name="gridUrl", default=None
                    ),
                ),
                (
                    "grid_url__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="gridUrl_Icontains", default=None
                    ),
                ),
                (
                    "grid_url__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="gridUrl_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    cdn_url = sgqlc.types.Field(String, graphql_name="cdnUrl")
    versions = sgqlc.types.Field("VersionsType", graphql_name="versions")
    all_apps = sgqlc.types.Field(
        sgqlc.types.list_of(AppType),
        graphql_name="allApps",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),)
        ),
    )
    active_apps = sgqlc.types.Field(
        sgqlc.types.list_of(AppType),
        graphql_name="activeApps",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),)
        ),
    )


class SecretType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "created", "modified", "name", "value")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    value = sgqlc.types.Field(JSONString, graphql_name="value")


class SubscriptionComponentType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "limits", "unit_price", "component")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    limits = sgqlc.types.Field(JSONString, graphql_name="limits")
    unit_price = sgqlc.types.Field(MoneyType, graphql_name="unitPrice")
    component = sgqlc.types.Field(ComponentType, graphql_name="component")


class SubscriptionType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "next_billing_date", "product", "components")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    next_billing_date = sgqlc.types.Field(
        DateTime, graphql_name="nextBillingDate"
    )
    product = sgqlc.types.Field(ProductType, graphql_name="product")
    components = sgqlc.types.Field(
        sgqlc.types.list_of(SubscriptionComponentType),
        graphql_name="components",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_type",
                    sgqlc.types.Arg(
                        AppTypeEnum, graphql_name="appType", default=None
                    ),
                ),
            )
        ),
    )


class TeamCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team",)
    team = sgqlc.types.Field("TeamType", graphql_name="team")


class TeamDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team",)
    team = sgqlc.types.Field("TeamType", graphql_name="team")


class TeamMemberAddMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team_member", "user")
    team_member = sgqlc.types.Field(
        "TeamMemberType", graphql_name="teamMember"
    )
    user = sgqlc.types.Field("UserType", graphql_name="user")


class TeamMemberRemoveAllMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field("UserType", graphql_name="user")


class TeamMemberRemoveMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team_member",)
    team_member = sgqlc.types.Field(
        "TeamMemberType", graphql_name="teamMember"
    )


class TeamMemberType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "created", "modified", "team", "user")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    team = sgqlc.types.Field("TeamType", graphql_name="team")
    user = sgqlc.types.Field("UserType", graphql_name="user")


class TeamType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "account",
        "name",
        "users",
        "team_members",
        "permission_set",
        "eligible_new_users",
        "app_teams",
        "apps",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    account = sgqlc.types.Field(
        sgqlc.types.non_null(AccountType), graphql_name="account"
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    users = sgqlc.types.Field(
        sgqlc.types.list_of("UserType"),
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "email",
                    sgqlc.types.Arg(
                        String, graphql_name="email", default=None
                    ),
                ),
                (
                    "email__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="email_Icontains", default=None
                    ),
                ),
                (
                    "email__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="email_Istartswith", default=None
                    ),
                ),
                (
                    "full_name",
                    sgqlc.types.Arg(
                        String, graphql_name="fullName", default=None
                    ),
                ),
                (
                    "full_name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="fullName_Icontains", default=None
                    ),
                ),
                (
                    "full_name__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="fullName_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    team_members = sgqlc.types.Field(
        sgqlc.types.list_of(TeamMemberType),
        graphql_name="teamMembers",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "team__id",
                    sgqlc.types.Arg(ID, graphql_name="team_Id", default=None),
                ),
                (
                    "team__name",
                    sgqlc.types.Arg(
                        String, graphql_name="team_Name", default=None
                    ),
                ),
                (
                    "team__name__icontains",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="team_Name_Icontains",
                        default=None,
                    ),
                ),
                (
                    "team__name__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="team_Name_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "team__account__id",
                    sgqlc.types.Arg(
                        ID, graphql_name="team_Account_Id", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    permission_set = sgqlc.types.Field(
        PermissionSetType, graphql_name="permissionSet"
    )
    eligible_new_users = sgqlc.types.Field(
        sgqlc.types.list_of("UserType"),
        graphql_name="eligibleNewUsers",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "email",
                    sgqlc.types.Arg(
                        String, graphql_name="email", default=None
                    ),
                ),
                (
                    "email__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="email_Icontains", default=None
                    ),
                ),
                (
                    "email__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="email_Istartswith", default=None
                    ),
                ),
                (
                    "full_name",
                    sgqlc.types.Arg(
                        String, graphql_name="fullName", default=None
                    ),
                ),
                (
                    "full_name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="fullName_Icontains", default=None
                    ),
                ),
                (
                    "full_name__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="fullName_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    app_teams = sgqlc.types.Field(
        sgqlc.types.list_of(AppTeamType),
        graphql_name="appTeams",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "app__id",
                    sgqlc.types.Arg(ID, graphql_name="app_Id", default=None),
                ),
                (
                    "team__id",
                    sgqlc.types.Arg(ID, graphql_name="team_Id", default=None),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    apps = sgqlc.types.Field(
        sgqlc.types.list_of(AppType),
        graphql_name="apps",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )


class TeamUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team", "permission_set")
    team = sgqlc.types.Field(TeamType, graphql_name="team")
    permission_set = sgqlc.types.Field(
        PermissionSetType, graphql_name="permissionSet"
    )


class TwitterCreateWelcomeMessageMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("response",)
    response = sgqlc.types.Field(JSONString, graphql_name="response")


class TwitterCreateWelcomeMessageRuleMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("response",)
    response = sgqlc.types.Field(JSONString, graphql_name="response")


class TwitterDeleteWebhookRegistryMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TwitterDeleteWelcomeMessageMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TwitterDeleteWelcomeMessageRuleMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TwitterListSubscriptionsMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("response",)
    response = sgqlc.types.Field(JSONString, graphql_name="response")


class TwitterListWebhooksMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("response",)
    response = sgqlc.types.Field(JSONString, graphql_name="response")


class TwitterListWelcomeMessageMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("response",)
    response = sgqlc.types.Field(JSONString, graphql_name="response")


class TwitterListWelcomeMessageRuleMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("response",)
    response = sgqlc.types.Field(JSONString, graphql_name="response")


class TwitterRegistryWebhookMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class UserRefreshAuthTokenMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field("UserType", graphql_name="user")


class UserType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "email",
        "full_name",
        "is_staff",
        "flow_editor_mode",
        "visual_scroll_mode",
        "editor_advanced_mode",
        "editor_simulator_opened",
        "accounts",
        "teams",
        "team_members",
        "token",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    full_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="fullName"
    )
    is_staff = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isStaff"
    )
    flow_editor_mode = sgqlc.types.Field(
        UserFlowEditorMode, graphql_name="flowEditorMode"
    )
    visual_scroll_mode = sgqlc.types.Field(
        UserVisualScrollMode, graphql_name="visualScrollMode"
    )
    editor_advanced_mode = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="editorAdvancedMode"
    )
    editor_simulator_opened = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="editorSimulatorOpened"
    )
    accounts = sgqlc.types.Field(
        sgqlc.types.list_of(AccountType),
        graphql_name="accounts",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    teams = sgqlc.types.Field(
        sgqlc.types.list_of(TeamType),
        graphql_name="teams",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "name__icontains",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Icontains", default=None
                    ),
                ),
                (
                    "name__istartswith",
                    sgqlc.types.Arg(
                        String, graphql_name="name_Istartswith", default=None
                    ),
                ),
                (
                    "account__id",
                    sgqlc.types.Arg(
                        ID, graphql_name="account_Id", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    team_members = sgqlc.types.Field(
        sgqlc.types.list_of(TeamMemberType),
        graphql_name="teamMembers",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "team__id",
                    sgqlc.types.Arg(ID, graphql_name="team_Id", default=None),
                ),
                (
                    "team__name",
                    sgqlc.types.Arg(
                        String, graphql_name="team_Name", default=None
                    ),
                ),
                (
                    "team__name__icontains",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="team_Name_Icontains",
                        default=None,
                    ),
                ),
                (
                    "team__name__istartswith",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="team_Name_Istartswith",
                        default=None,
                    ),
                ),
                (
                    "team__account__id",
                    sgqlc.types.Arg(
                        ID, graphql_name="team_Account_Id", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
            )
        ),
    )
    token = sgqlc.types.Field(String, graphql_name="token")


class UserUpdateEditorAdvancedModeMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field(UserType, graphql_name="user")


class UserUpdateEditorSimulatorOpenedMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field(UserType, graphql_name="user")


class UserUpdateFlowEditorModeMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field(UserType, graphql_name="user")


class UserUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field(UserType, graphql_name="user")


class UserUpdateVisualScrollModeMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("user",)
    user = sgqlc.types.Field(UserType, graphql_name="user")


class VersionsType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("grid", "console", "meya_sdk", "meya_cli")
    grid = sgqlc.types.Field(String, graphql_name="grid")
    console = sgqlc.types.Field(String, graphql_name="console")
    meya_sdk = sgqlc.types.Field(String, graphql_name="meyaSdk")
    meya_cli = sgqlc.types.Field(String, graphql_name="meyaCli")


class AppUserType(sgqlc.types.Type, Node):
    __schema__ = schema
    __field_names__ = (
        "app_id",
        "created",
        "modified",
        "data",
        "user_id",
        "type",
        "name",
        "email",
    )
    app_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="appId"
    )
    created = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="created"
    )
    modified = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="modified"
    )
    data = sgqlc.types.Field(
        sgqlc.types.non_null(JSONString), graphql_name="data"
    )
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="userId"
    )
    type = sgqlc.types.Field(String, graphql_name="type")
    name = sgqlc.types.Field(String, graphql_name="name")
    email = sgqlc.types.Field(String, graphql_name="email")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = None
