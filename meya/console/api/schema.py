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


class CardType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "VISA",
        "MASTER",
        "DISCOVER",
        "AMERICAN_EXPRESS",
        "DINERS_CLUB",
        "JCB",
        "SWITCH",
        "SOLO",
        "DANKFORT",
        "MAESTRO",
        "LASER",
        "FORBRUGSFORENINGEN",
    )


class CurrentVault(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("AUTHORIZENET", "STRIPE")


class DataSourceType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "WEB_CRAWLER",
        "SITEMAP",
        "URL_LIST",
        "TEXT",
        "ZENDESK_HELP_CENTER",
        "NOTION",
    )


DateTime = sgqlc.types.datetime.DateTime

Float = sgqlc.types.Float

ID = sgqlc.types.ID


class IndexType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("VECTOR",)


Int = sgqlc.types.Int


class InviteState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("CREATED", "PENDING", "RESENT", "REVOKED")


class ItemIndexState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("FAILED", "INDEXED", "INDEXING", "QUEUED", "NOT_INDEXED")


class ItemType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("WEB_PAGE", "TEXT", "INTENT")


class JSONString(sgqlc.types.Scalar):
    __schema__ = schema


class JobState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "CANCELLED",
        "COMPLETE",
        "CRAWLING",
        "IMPORTING",
        "FAILED",
        "INDEXING",
        "QUEUED",
        "RUNNING",
    )


class JobType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("IMPORT_DATA", "INDEX_ITEMS")


class LlmProvider(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("OPENAI",)


class Money(sgqlc.types.Scalar):
    __schema__ = schema


class OpenaiTextModel(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "GPT_4",
        "GPT_4_0314",
        "GPT_4_32K",
        "GPT_4_32K_0314",
        "GPT_3_5_TURBO_0301",
        "GPT_3_5_TURBO",
        "TEXT_DAVINCI_003",
        "TEXT_DAVINCI_002",
        "TEXT_CURIE_001",
        "TEXT_BABBAGE_001",
        "TEXT_ADA_001",
    )


class PaymentType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ("CREDIT_CARD", "BANK_ACCOUNT", "PAYPAL_ACCOUNT")


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


class SubscriptionState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = (
        "ACTIVE",
        "CANCELED",
        "EXPIRED",
        "ON_HOLD",
        "PAST_DUE",
        "SOFT_FAILURE",
        "TRIALING",
        "TRIAL_ENDED",
        "UNPAID",
        "SUSPENDED",
        "AWAITING_SIGNUP",
        "ASSESSING",
        "FAILED_TO_CREATE",
        "PAUSED",
        "PENDING",
    )


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


class CreateTrainingDataSourceInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("name", "app_id", "config", "data_source_type")
    name = sgqlc.types.Field(String, graphql_name="name")
    app_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="appId")
    config = sgqlc.types.Field(
        sgqlc.types.non_null(JSONString), graphql_name="config"
    )
    data_source_type = sgqlc.types.Field(
        sgqlc.types.non_null(DataSourceType), graphql_name="dataSourceType"
    )


class CreateTrainingItemInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = (
        "app_id",
        "item_type",
        "source_ref",
        "data",
        "tags",
        "data_source_id",
    )
    app_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="appId")
    item_type = sgqlc.types.Field(ItemType, graphql_name="itemType")
    source_ref = sgqlc.types.Field(String, graphql_name="sourceRef")
    data = sgqlc.types.Field(JSONString, graphql_name="data")
    tags = sgqlc.types.Field(JSONString, graphql_name="tags")
    data_source_id = sgqlc.types.Field(ID, graphql_name="dataSourceId")


class CustomerInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = (
        "first_name",
        "last_name",
        "email",
        "cc_emails",
        "phone",
        "organization",
        "address",
        "address2",
        "city",
        "state",
        "state_name",
        "zip",
        "country",
        "country_name",
        "vat_number",
    )
    first_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="firstName"
    )
    last_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="lastName"
    )
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    cc_emails = sgqlc.types.Field(String, graphql_name="ccEmails")
    phone = sgqlc.types.Field(String, graphql_name="phone")
    organization = sgqlc.types.Field(String, graphql_name="organization")
    address = sgqlc.types.Field(String, graphql_name="address")
    address2 = sgqlc.types.Field(String, graphql_name="address2")
    city = sgqlc.types.Field(String, graphql_name="city")
    state = sgqlc.types.Field(String, graphql_name="state")
    state_name = sgqlc.types.Field(String, graphql_name="stateName")
    zip = sgqlc.types.Field(String, graphql_name="zip")
    country = sgqlc.types.Field(String, graphql_name="country")
    country_name = sgqlc.types.Field(String, graphql_name="countryName")
    vat_number = sgqlc.types.Field(String, graphql_name="vatNumber")


class LlmPromptTemplateInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = (
        "app_id",
        "name",
        "version",
        "active",
        "text",
        "model",
        "provider",
        "hyperparameters",
    )
    app_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="appId")
    name = sgqlc.types.Field(String, graphql_name="name")
    version = sgqlc.types.Field(String, graphql_name="version")
    active = sgqlc.types.Field(Boolean, graphql_name="active")
    text = sgqlc.types.Field(String, graphql_name="text")
    model = sgqlc.types.Field(OpenaiTextModel, graphql_name="model")
    provider = sgqlc.types.Field(LlmProvider, graphql_name="provider")
    hyperparameters = sgqlc.types.Field(
        JSONString, graphql_name="hyperparameters"
    )


class PaymentProfileInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = (
        "chargify_token",
        "billing_address",
        "billing_address2",
        "billing_city",
        "billing_state",
        "billing_zip",
        "billing_country",
    )
    chargify_token = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="chargifyToken"
    )
    billing_address = sgqlc.types.Field(String, graphql_name="billingAddress")
    billing_address2 = sgqlc.types.Field(
        String, graphql_name="billingAddress2"
    )
    billing_city = sgqlc.types.Field(String, graphql_name="billingCity")
    billing_state = sgqlc.types.Field(String, graphql_name="billingState")
    billing_zip = sgqlc.types.Field(String, graphql_name="billingZip")
    billing_country = sgqlc.types.Field(String, graphql_name="billingCountry")


class TrainingDataSourceInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("name", "app_id", "config", "data_source_type")
    name = sgqlc.types.Field(String, graphql_name="name")
    app_id = sgqlc.types.Field(ID, graphql_name="appId")
    config = sgqlc.types.Field(
        sgqlc.types.non_null(JSONString), graphql_name="config"
    )
    data_source_type = sgqlc.types.Field(
        DataSourceType, graphql_name="dataSourceType"
    )


class TrainingIndexInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("app_id", "config", "index_type")
    app_id = sgqlc.types.Field(ID, graphql_name="appId")
    config = sgqlc.types.Field(
        sgqlc.types.non_null(JSONString), graphql_name="config"
    )
    index_type = sgqlc.types.Field(IndexType, graphql_name="indexType")


class TrainingItemInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = (
        "app_id",
        "item_type",
        "source_ref",
        "data",
        "tags",
        "data_source_id",
    )
    app_id = sgqlc.types.Field(ID, graphql_name="appId")
    item_type = sgqlc.types.Field(ItemType, graphql_name="itemType")
    source_ref = sgqlc.types.Field(String, graphql_name="sourceRef")
    data = sgqlc.types.Field(JSONString, graphql_name="data")
    tags = sgqlc.types.Field(JSONString, graphql_name="tags")
    data_source_id = sgqlc.types.Field(ID, graphql_name="dataSourceId")


########################################################################
# Output Objects and Interfaces
########################################################################
class AccountCancelMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("account",)
    account = sgqlc.types.Field("AccountType", graphql_name="account")


class AccountDisableMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("account",)
    account = sgqlc.types.Field("AccountType", graphql_name="account")


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


class AccountReactivateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("account",)
    account = sgqlc.types.Field("AccountType", graphql_name="account")


class AccountType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
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
        "customer",
        "subscriptions",
        "subscription",
        "usage_subscription",
        "components",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
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
    customer = sgqlc.types.Field("CustomerType", graphql_name="customer")
    subscriptions = sgqlc.types.Field(
        sgqlc.types.list_of("SubscriptionType"), graphql_name="subscriptions"
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


class AiJobCancelMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("job",)
    job = sgqlc.types.Field("AiJobType", graphql_name="job")


class AiJobType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "job_type",
        "state",
        "state_message",
        "app",
        "data_source",
        "logs",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    job_type = sgqlc.types.Field(JobType, graphql_name="jobType")
    state = sgqlc.types.Field(JobState, graphql_name="state")
    state_message = sgqlc.types.Field(String, graphql_name="stateMessage")
    app = sgqlc.types.Field("AppType", graphql_name="app")
    data_source = sgqlc.types.Field(
        "TrainingDataSourceType", graphql_name="dataSource"
    )
    logs = sgqlc.types.Field(String, graphql_name="logs")


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
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


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
        "modified",
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
        "webhook_url",
        "training_data_sources",
        "training_index",
        "ai_jobs",
        "last_index_ai_job",
        "llm_prompt_templates",
        "default_llm_prompt_templates",
        "training_items",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
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
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "next_revision",
                    sgqlc.types.Arg(
                        String, graphql_name="nextRevision", default=None
                    ),
                ),
                (
                    "state",
                    sgqlc.types.Arg(
                        String, graphql_name="state", default=None
                    ),
                ),
                (
                    "user__id",
                    sgqlc.types.Arg(ID, graphql_name="user_Id", default=None),
                ),
                (
                    "push_type",
                    sgqlc.types.Arg(
                        String, graphql_name="pushType", default=None
                    ),
                ),
                (
                    "app_type",
                    sgqlc.types.Arg(
                        String, graphql_name="appType", default=None
                    ),
                ),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        String, graphql_name="orderBy", default=None
                    ),
                ),
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
    webhook_url = sgqlc.types.Field(
        String,
        graphql_name="webhookUrl",
        args=sgqlc.types.ArgDict(
            (
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
    training_data_sources = sgqlc.types.Field(
        sgqlc.types.list_of("TrainingDataSourceType"),
        graphql_name="trainingDataSources",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "data_source_type",
                    sgqlc.types.Arg(
                        String, graphql_name="dataSourceType", default=None
                    ),
                ),
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
    training_index = sgqlc.types.Field(
        "TrainingIndexType", graphql_name="trainingIndex"
    )
    ai_jobs = sgqlc.types.Field(
        sgqlc.types.list_of(AiJobType),
        graphql_name="aiJobs",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "offset",
                    sgqlc.types.Arg(Int, graphql_name="offset", default=None),
                ),
                (
                    "limit",
                    sgqlc.types.Arg(Int, graphql_name="limit", default=None),
                ),
                (
                    "job_type",
                    sgqlc.types.Arg(
                        JobType, graphql_name="jobType", default=None
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
    last_index_ai_job = sgqlc.types.Field(
        AiJobType, graphql_name="lastIndexAiJob"
    )
    llm_prompt_templates = sgqlc.types.Field(
        sgqlc.types.list_of("LlmPromptTemplateType"),
        graphql_name="llmPromptTemplates",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "active",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="active", default=None
                    ),
                ),
                (
                    "app_id",
                    sgqlc.types.Arg(ID, graphql_name="appId", default=None),
                ),
                (
                    "app_id__in",
                    sgqlc.types.Arg(ID, graphql_name="appId_In", default=None),
                ),
                (
                    "version",
                    sgqlc.types.Arg(
                        String, graphql_name="version", default=None
                    ),
                ),
                (
                    "version__in",
                    sgqlc.types.Arg(
                        String, graphql_name="version_In", default=None
                    ),
                ),
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
    default_llm_prompt_templates = sgqlc.types.Field(
        sgqlc.types.list_of("LlmPromptTemplateType"),
        graphql_name="defaultLlmPromptTemplates",
    )
    training_items = sgqlc.types.Field(
        "TrainingItemsType",
        graphql_name="trainingItems",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "offset",
                    sgqlc.types.Arg(Int, graphql_name="offset", default=None),
                ),
                (
                    "limit",
                    sgqlc.types.Arg(Int, graphql_name="limit", default=None),
                ),
                (
                    "source_ref",
                    sgqlc.types.Arg(
                        String, graphql_name="sourceRef", default=None
                    ),
                ),
                (
                    "source_ref__icontains",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="sourceRef_Icontains",
                        default=None,
                    ),
                ),
                (
                    "item_type",
                    sgqlc.types.Arg(
                        ItemType, graphql_name="itemType", default=None
                    ),
                ),
                (
                    "data_source_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(ID),
                        graphql_name="dataSourceIds",
                        default=None,
                    ),
                ),
                (
                    "data_source_type",
                    sgqlc.types.Arg(
                        DataSourceType,
                        graphql_name="dataSourceType",
                        default=None,
                    ),
                ),
                (
                    "index_state",
                    sgqlc.types.Arg(
                        ItemIndexState, graphql_name="indexState", default=None
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


class CreatePaymentProfileMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("payment_profile_or_error",)
    payment_profile_or_error = sgqlc.types.Field(
        "CreatePaymentMethodResultType", graphql_name="paymentProfileOrError"
    )


class CreditCardType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "first_name",
        "last_name",
        "masked_card_number",
        "card_type",
        "expiration_month",
        "expiration_year",
        "customer_id",
        "current_vault",
        "vault_token",
        "billing_address",
        "billing_address2",
        "billing_city",
        "billing_state",
        "billing_zip",
        "billing_country",
        "customer_vault_token",
        "payment_type",
        "disabled",
        "chargify_token",
        "site_gateway_setting_id",
        "gateway_handle",
    )
    id = sgqlc.types.Field(Int, graphql_name="id")
    first_name = sgqlc.types.Field(String, graphql_name="firstName")
    last_name = sgqlc.types.Field(String, graphql_name="lastName")
    masked_card_number = sgqlc.types.Field(
        String, graphql_name="maskedCardNumber"
    )
    card_type = sgqlc.types.Field(CardType, graphql_name="cardType")
    expiration_month = sgqlc.types.Field(Int, graphql_name="expirationMonth")
    expiration_year = sgqlc.types.Field(Int, graphql_name="expirationYear")
    customer_id = sgqlc.types.Field(Int, graphql_name="customerId")
    current_vault = sgqlc.types.Field(
        CurrentVault, graphql_name="currentVault"
    )
    vault_token = sgqlc.types.Field(String, graphql_name="vaultToken")
    billing_address = sgqlc.types.Field(String, graphql_name="billingAddress")
    billing_address2 = sgqlc.types.Field(
        String, graphql_name="billingAddress2"
    )
    billing_city = sgqlc.types.Field(String, graphql_name="billingCity")
    billing_state = sgqlc.types.Field(String, graphql_name="billingState")
    billing_zip = sgqlc.types.Field(String, graphql_name="billingZip")
    billing_country = sgqlc.types.Field(String, graphql_name="billingCountry")
    customer_vault_token = sgqlc.types.Field(
        String, graphql_name="customerVaultToken"
    )
    payment_type = sgqlc.types.Field(String, graphql_name="paymentType")
    disabled = sgqlc.types.Field(Boolean, graphql_name="disabled")
    chargify_token = sgqlc.types.Field(String, graphql_name="chargifyToken")
    site_gateway_setting_id = sgqlc.types.Field(
        Int, graphql_name="siteGatewaySettingId"
    )
    gateway_handle = sgqlc.types.Field(String, graphql_name="gatewayHandle")


class CustomerType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "email",
        "first_name",
        "last_name",
        "cc_emails",
        "phone",
        "organization",
        "address",
        "address2",
        "city",
        "state",
        "state_name",
        "zip",
        "country",
        "country_name",
        "tax_exempt",
        "vat_number",
        "reference",
        "chargify_server_host",
        "chargify_public_key",
        "chargify_security_token",
        "payment_profiles",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    first_name = sgqlc.types.Field(String, graphql_name="firstName")
    last_name = sgqlc.types.Field(String, graphql_name="lastName")
    cc_emails = sgqlc.types.Field(String, graphql_name="ccEmails")
    phone = sgqlc.types.Field(String, graphql_name="phone")
    organization = sgqlc.types.Field(String, graphql_name="organization")
    address = sgqlc.types.Field(String, graphql_name="address")
    address2 = sgqlc.types.Field(String, graphql_name="address2")
    city = sgqlc.types.Field(String, graphql_name="city")
    state = sgqlc.types.Field(String, graphql_name="state")
    state_name = sgqlc.types.Field(String, graphql_name="stateName")
    zip = sgqlc.types.Field(String, graphql_name="zip")
    country = sgqlc.types.Field(String, graphql_name="country")
    country_name = sgqlc.types.Field(String, graphql_name="countryName")
    tax_exempt = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="taxExempt"
    )
    vat_number = sgqlc.types.Field(String, graphql_name="vatNumber")
    reference = sgqlc.types.Field(String, graphql_name="reference")
    chargify_server_host = sgqlc.types.Field(
        String, graphql_name="chargifyServerHost"
    )
    chargify_public_key = sgqlc.types.Field(
        String, graphql_name="chargifyPublicKey"
    )
    chargify_security_token = sgqlc.types.Field(
        String, graphql_name="chargifySecurityToken"
    )
    payment_profiles = sgqlc.types.Field(
        sgqlc.types.list_of("PaymentProfileType"),
        graphql_name="paymentProfiles",
    )


class CustomerUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("customer_or_error",)
    customer_or_error = sgqlc.types.Field(
        "UpdateCustomerResultType", graphql_name="customerOrError"
    )


class DefaultPaymentProfileUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("payment_profile",)
    payment_profile = sgqlc.types.Field(
        "PaymentProfileType", graphql_name="paymentProfile"
    )


class GatewayPushMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("result",)
    result = sgqlc.types.Field(String, graphql_name="result")


class InputErrorType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("message", "field_errors")
    message = sgqlc.types.Field(String, graphql_name="message")
    field_errors = sgqlc.types.Field(
        sgqlc.types.list_of("InputFieldError"), graphql_name="fieldErrors"
    )


class InputFieldError(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("name", "message", "error")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    message = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="message"
    )
    error = sgqlc.types.Field(JSONString, graphql_name="error")


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


class LlmPromptTemplateCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("llm_prompt_template_or_error",)
    llm_prompt_template_or_error = sgqlc.types.Field(
        "LlmPromptTemplateResultType", graphql_name="llmPromptTemplateOrError"
    )


class LlmPromptTemplateDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class LlmPromptTemplateType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "name",
        "version",
        "active",
        "text",
        "model",
        "provider",
        "hyperparameters",
        "metadata",
        "app_id",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    version = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="version"
    )
    active = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="active"
    )
    text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="text")
    model = sgqlc.types.Field(OpenaiTextModel, graphql_name="model")
    provider = sgqlc.types.Field(LlmProvider, graphql_name="provider")
    hyperparameters = sgqlc.types.Field(
        JSONString, graphql_name="hyperparameters"
    )
    metadata = sgqlc.types.Field(JSONString, graphql_name="metadata")
    app_id = sgqlc.types.Field(ID, graphql_name="appId")


class LlmPromptTemplateUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("llm_prompt_template_or_error",)
    llm_prompt_template_or_error = sgqlc.types.Field(
        "LlmPromptTemplateResultType", graphql_name="llmPromptTemplateOrError"
    )


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
        "disable_account",
        "cancel_account",
        "reactivate_account",
        "update_customer",
        "create_payment_profile",
        "update_default_payment_profile",
        "update_app",
        "create_app",
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
        "cancel_ai_job",
        "update_training_data_source",
        "create_training_data_source",
        "delete_training_data_source",
        "delete_training_data_source_items",
        "update_training_item",
        "create_training_item",
        "delete_training_item",
        "update_training_index",
        "clear_training_index",
        "import_training_data",
        "index_training_items",
        "import_and_index_training_items",
        "update_llm_prompt_template",
        "create_llm_prompt_template",
        "delete_llm_prompt_template",
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
        "openai_verify_api_key",
        "zendesk_verify_api_token",
        "notion_verify_api_token",
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
    disable_account = sgqlc.types.Field(
        AccountDisableMutation,
        graphql_name="disableAccount",
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
    cancel_account = sgqlc.types.Field(
        AccountCancelMutation,
        graphql_name="cancelAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cancellation_message",
                    sgqlc.types.Arg(
                        String,
                        graphql_name="cancellationMessage",
                        default=None,
                    ),
                ),
                (
                    "delayed",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="delayed",
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
                    "reason_code",
                    sgqlc.types.Arg(
                        String, graphql_name="reasonCode", default=None
                    ),
                ),
            )
        ),
    )
    reactivate_account = sgqlc.types.Field(
        AccountReactivateMutation,
        graphql_name="reactivateAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "coupon_code",
                    sgqlc.types.Arg(
                        String, graphql_name="couponCode", default=None
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
    update_customer = sgqlc.types.Field(
        CustomerUpdateMutation,
        graphql_name="updateCustomer",
        args=sgqlc.types.ArgDict(
            (
                (
                    "customer",
                    sgqlc.types.Arg(
                        CustomerInput, graphql_name="customer", default=None
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
    create_payment_profile = sgqlc.types.Field(
        CreatePaymentProfileMutation,
        graphql_name="createPaymentProfile",
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
                    "payment_profile",
                    sgqlc.types.Arg(
                        PaymentProfileInput,
                        graphql_name="paymentProfile",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_default_payment_profile = sgqlc.types.Field(
        DefaultPaymentProfileUpdateMutation,
        graphql_name="updateDefaultPaymentProfile",
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
                    "payment_profile_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="paymentProfileId",
                        default=None,
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
        "PushCancelMutation",
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
    cancel_ai_job = sgqlc.types.Field(
        AiJobCancelMutation,
        graphql_name="cancelAiJob",
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
    update_training_data_source = sgqlc.types.Field(
        "TrainingDataSourceUpdateMutation",
        graphql_name="updateTrainingDataSource",
        args=sgqlc.types.ArgDict(
            (
                (
                    "data_source",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(TrainingDataSourceInput),
                        graphql_name="dataSource",
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
    create_training_data_source = sgqlc.types.Field(
        "TrainingDataSourceCreateMutation",
        graphql_name="createTrainingDataSource",
        args=sgqlc.types.ArgDict(
            (
                (
                    "data_source",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(CreateTrainingDataSourceInput),
                        graphql_name="dataSource",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_training_data_source = sgqlc.types.Field(
        "TrainingDataSourceDeleteMutation",
        graphql_name="deleteTrainingDataSource",
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
    delete_training_data_source_items = sgqlc.types.Field(
        "TrainingDataSourceDeleteItemsMutation",
        graphql_name="deleteTrainingDataSourceItems",
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
    update_training_item = sgqlc.types.Field(
        "TrainingItemUpdateMutation",
        graphql_name="updateTrainingItem",
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
                    "item",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(TrainingItemInput),
                        graphql_name="item",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_training_item = sgqlc.types.Field(
        "TrainingItemCreateMutation",
        graphql_name="createTrainingItem",
        args=sgqlc.types.ArgDict(
            (
                (
                    "item",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(CreateTrainingItemInput),
                        graphql_name="item",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_training_item = sgqlc.types.Field(
        "TrainingItemDeleteMutation",
        graphql_name="deleteTrainingItem",
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
    update_training_index = sgqlc.types.Field(
        "TrainingIndexUpdateMutation",
        graphql_name="updateTrainingIndex",
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
                    "index",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(TrainingIndexInput),
                        graphql_name="index",
                        default=None,
                    ),
                ),
            )
        ),
    )
    clear_training_index = sgqlc.types.Field(
        "TrainingIndexClearMutation",
        graphql_name="clearTrainingIndex",
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
    import_training_data = sgqlc.types.Field(
        "TrainingImportDataMutation",
        graphql_name="importTrainingData",
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
                    "data_source_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(ID),
                        graphql_name="dataSourceIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    index_training_items = sgqlc.types.Field(
        "TrainingIndexItemsMutation",
        graphql_name="indexTrainingItems",
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
                    "data_source_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="dataSourceId", default=None
                    ),
                ),
                (
                    "item_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(ID),
                        graphql_name="itemIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_and_index_training_items = sgqlc.types.Field(
        "TrainingImportAndIndexMutation",
        graphql_name="importAndIndexTrainingItems",
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
                    "data_source_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(ID),
                        graphql_name="dataSourceIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_llm_prompt_template = sgqlc.types.Field(
        LlmPromptTemplateUpdateMutation,
        graphql_name="updateLlmPromptTemplate",
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
                    "llm_prompt_template",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(LlmPromptTemplateInput),
                        graphql_name="llmPromptTemplate",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_llm_prompt_template = sgqlc.types.Field(
        LlmPromptTemplateCreateMutation,
        graphql_name="createLlmPromptTemplate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "llm_prompt_template",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(LlmPromptTemplateInput),
                        graphql_name="llmPromptTemplate",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_llm_prompt_template = sgqlc.types.Field(
        LlmPromptTemplateDeleteMutation,
        graphql_name="deleteLlmPromptTemplate",
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
    openai_verify_api_key = sgqlc.types.Field(
        "OpenaiVerifyApiKeyMutation",
        graphql_name="openaiVerifyApiKey",
        args=sgqlc.types.ArgDict(
            (
                (
                    "api_key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="apiKey",
                        default=None,
                    ),
                ),
            )
        ),
    )
    zendesk_verify_api_token = sgqlc.types.Field(
        "ZendeskVerifyApiTokenMutation",
        graphql_name="zendeskVerifyApiToken",
        args=sgqlc.types.ArgDict(
            (
                (
                    "api_token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="apiToken",
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
                    "subdomain",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="subdomain",
                        default=None,
                    ),
                ),
            )
        ),
    )
    notion_verify_api_token = sgqlc.types.Field(
        "NotionVerifyApiTokenMutation",
        graphql_name="notionVerifyApiToken",
        args=sgqlc.types.ArgDict(
            (
                (
                    "api_token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="apiToken",
                        default=None,
                    ),
                ),
            )
        ),
    )


class Node(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class NotionVerifyApiTokenMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok", "error")
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")
    error = sgqlc.types.Field(String, graphql_name="error")


class OpenaiVerifyApiKeyMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok", "error")
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")
    error = sgqlc.types.Field(String, graphql_name="error")


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


class PaymentProfileType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "first_name",
        "last_name",
        "billing_address",
        "billing_address2",
        "billing_city",
        "billing_state",
        "billing_zip",
        "billing_country",
        "bank_name",
        "masked_bank_routing_number",
        "masked_bank_account_number",
        "bank_account_type",
        "payment_type",
        "verified",
        "masked_card_number",
        "card_type",
        "expiration_month",
        "expiration_year",
    )
    id = sgqlc.types.Field(Int, graphql_name="id")
    first_name = sgqlc.types.Field(String, graphql_name="firstName")
    last_name = sgqlc.types.Field(String, graphql_name="lastName")
    billing_address = sgqlc.types.Field(String, graphql_name="billingAddress")
    billing_address2 = sgqlc.types.Field(
        String, graphql_name="billingAddress2"
    )
    billing_city = sgqlc.types.Field(String, graphql_name="billingCity")
    billing_state = sgqlc.types.Field(String, graphql_name="billingState")
    billing_zip = sgqlc.types.Field(String, graphql_name="billingZip")
    billing_country = sgqlc.types.Field(String, graphql_name="billingCountry")
    bank_name = sgqlc.types.Field(String, graphql_name="bankName")
    masked_bank_routing_number = sgqlc.types.Field(
        String, graphql_name="maskedBankRoutingNumber"
    )
    masked_bank_account_number = sgqlc.types.Field(
        String, graphql_name="maskedBankAccountNumber"
    )
    bank_account_type = sgqlc.types.Field(
        String, graphql_name="bankAccountType"
    )
    payment_type = sgqlc.types.Field(PaymentType, graphql_name="paymentType")
    verified = sgqlc.types.Field(String, graphql_name="verified")
    masked_card_number = sgqlc.types.Field(
        String, graphql_name="maskedCardNumber"
    )
    card_type = sgqlc.types.Field(CardType, graphql_name="cardType")
    expiration_month = sgqlc.types.Field(Int, graphql_name="expirationMonth")
    expiration_year = sgqlc.types.Field(Int, graphql_name="expirationYear")


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
    __field_names__ = ("id", "name", "limits", "require_billing_address")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    limits = sgqlc.types.Field(JSONString, graphql_name="limits")
    require_billing_address = sgqlc.types.Field(
        Boolean, graphql_name="requireBillingAddress"
    )


class PushCancelMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("push",)
    push = sgqlc.types.Field("PushType", graphql_name="push")


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
        "llm_prompt_templates",
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
    llm_prompt_templates = sgqlc.types.Field(
        sgqlc.types.list_of(LlmPromptTemplateType),
        graphql_name="llmPromptTemplates",
        args=sgqlc.types.ArgDict(
            (
                (
                    "app_id",
                    sgqlc.types.Arg(ID, graphql_name="appId", default=None),
                ),
            )
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
    __field_names__ = (
        "id",
        "next_billing_date",
        "state",
        "cancel_at_end_of_period",
        "product",
        "components",
        "product_price",
        "credit_card",
        "has_credit_card",
        "is_credit_card_expired",
        "days_to_credit_card_expired",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    next_billing_date = sgqlc.types.Field(
        DateTime, graphql_name="nextBillingDate"
    )
    state = sgqlc.types.Field(
        SubscriptionState,
        graphql_name="state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "refresh",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="refresh", default=None
                    ),
                ),
            )
        ),
    )
    cancel_at_end_of_period = sgqlc.types.Field(
        Boolean, graphql_name="cancelAtEndOfPeriod"
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
    product_price = sgqlc.types.Field(MoneyType, graphql_name="productPrice")
    credit_card = sgqlc.types.Field(CreditCardType, graphql_name="creditCard")
    has_credit_card = sgqlc.types.Field(Boolean, graphql_name="hasCreditCard")
    is_credit_card_expired = sgqlc.types.Field(
        Boolean, graphql_name="isCreditCardExpired"
    )
    days_to_credit_card_expired = sgqlc.types.Field(
        Int, graphql_name="daysToCreditCardExpired"
    )


class TeamCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team",)
    team = sgqlc.types.Field("TeamType", graphql_name="team")


class TeamDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


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


class TeamUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("team", "permission_set")
    team = sgqlc.types.Field(TeamType, graphql_name="team")
    permission_set = sgqlc.types.Field(
        PermissionSetType, graphql_name="permissionSet"
    )


class TrainingDataSourceAnalyticsType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("total_items",)
    total_items = sgqlc.types.Field(Int, graphql_name="totalItems")


class TrainingDataSourceCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("data_source_or_error",)
    data_source_or_error = sgqlc.types.Field(
        "TrainingDataSourceResultType", graphql_name="dataSourceOrError"
    )


class TrainingDataSourceDeleteItemsMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TrainingDataSourceDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TrainingDataSourceType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "data_source_type",
        "name",
        "config",
        "jobs",
        "last_job",
        "analytics",
        "zendesk_help_center",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    data_source_type = sgqlc.types.Field(
        DataSourceType, graphql_name="dataSourceType"
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    config = sgqlc.types.Field(JSONString, graphql_name="config")
    jobs = sgqlc.types.Field(
        sgqlc.types.list_of(AiJobType),
        graphql_name="jobs",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "offset",
                    sgqlc.types.Arg(Int, graphql_name="offset", default=None),
                ),
                (
                    "limit",
                    sgqlc.types.Arg(Int, graphql_name="limit", default=None),
                ),
                (
                    "job_type",
                    sgqlc.types.Arg(
                        JobType, graphql_name="jobType", default=None
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
    last_job = sgqlc.types.Field(
        AiJobType,
        graphql_name="lastJob",
        args=sgqlc.types.ArgDict(
            (
                (
                    "job_type",
                    sgqlc.types.Arg(
                        JobType, graphql_name="jobType", default=None
                    ),
                ),
            )
        ),
    )
    analytics = sgqlc.types.Field(
        TrainingDataSourceAnalyticsType, graphql_name="analytics"
    )
    zendesk_help_center = sgqlc.types.Field(
        "ZendeskHelpCenterType", graphql_name="zendeskHelpCenter"
    )


class TrainingDataSourceUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("data_source_or_error",)
    data_source_or_error = sgqlc.types.Field(
        "TrainingDataSourceResultType", graphql_name="dataSourceOrError"
    )


class TrainingImportAndIndexMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("jobs",)
    jobs = sgqlc.types.Field(
        sgqlc.types.list_of(AiJobType), graphql_name="jobs"
    )


class TrainingImportDataMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("jobs",)
    jobs = sgqlc.types.Field(
        sgqlc.types.list_of(AiJobType), graphql_name="jobs"
    )


class TrainingIndexClearMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TrainingIndexItemsMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("job",)
    job = sgqlc.types.Field(AiJobType, graphql_name="job")


class TrainingIndexType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "index_type",
        "config",
        "jobs",
        "last_job",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    index_type = sgqlc.types.Field(IndexType, graphql_name="indexType")
    config = sgqlc.types.Field(JSONString, graphql_name="config")
    jobs = sgqlc.types.Field(
        sgqlc.types.list_of(AiJobType),
        graphql_name="jobs",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "offset",
                    sgqlc.types.Arg(Int, graphql_name="offset", default=None),
                ),
                (
                    "limit",
                    sgqlc.types.Arg(Int, graphql_name="limit", default=None),
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
    last_job = sgqlc.types.Field(AiJobType, graphql_name="lastJob")


class TrainingIndexUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("index_or_error",)
    index_or_error = sgqlc.types.Field(
        "TrainingIndexResultType", graphql_name="indexOrError"
    )


class TrainingItemCreateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("item_or_error",)
    item_or_error = sgqlc.types.Field(
        "TrainingItemResultOrErrorType", graphql_name="itemOrError"
    )


class TrainingItemDeleteMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok",)
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")


class TrainingItemType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "id",
        "created",
        "modified",
        "item_type",
        "source_ref",
        "data",
        "tags",
        "index_state",
        "index_state_message",
        "data_source",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created = sgqlc.types.Field(DateTime, graphql_name="created")
    modified = sgqlc.types.Field(DateTime, graphql_name="modified")
    item_type = sgqlc.types.Field(ItemType, graphql_name="itemType")
    source_ref = sgqlc.types.Field(String, graphql_name="sourceRef")
    data = sgqlc.types.Field(JSONString, graphql_name="data")
    tags = sgqlc.types.Field(JSONString, graphql_name="tags")
    index_state = sgqlc.types.Field(ItemIndexState, graphql_name="indexState")
    index_state_message = sgqlc.types.Field(
        String, graphql_name="indexStateMessage"
    )
    data_source = sgqlc.types.Field(
        TrainingDataSourceType, graphql_name="dataSource"
    )


class TrainingItemUpdateMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("item_or_error",)
    item_or_error = sgqlc.types.Field(
        "TrainingItemResultOrErrorType", graphql_name="itemOrError"
    )


class TrainingItemsType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("total_items", "items")
    total_items = sgqlc.types.Field(Int, graphql_name="totalItems")
    items = sgqlc.types.Field(
        sgqlc.types.list_of(TrainingItemType), graphql_name="items"
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


class ZendeskHelpCenterCategoryType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(ID, graphql_name="id")
    name = sgqlc.types.Field(String, graphql_name="name")


class ZendeskHelpCenterLabelType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(ID, graphql_name="id")
    name = sgqlc.types.Field(String, graphql_name="name")


class ZendeskHelpCenterSectionType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(ID, graphql_name="id")
    name = sgqlc.types.Field(String, graphql_name="name")


class ZendeskHelpCenterType(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("labels", "categories", "sections")
    labels = sgqlc.types.Field(
        sgqlc.types.list_of(ZendeskHelpCenterLabelType), graphql_name="labels"
    )
    categories = sgqlc.types.Field(
        sgqlc.types.list_of(ZendeskHelpCenterCategoryType),
        graphql_name="categories",
    )
    sections = sgqlc.types.Field(
        sgqlc.types.list_of(ZendeskHelpCenterSectionType),
        graphql_name="sections",
        args=sgqlc.types.ArgDict(
            (
                (
                    "category_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="categoryId", default=None
                    ),
                ),
            )
        ),
    )


class ZendeskVerifyApiTokenMutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("ok", "error")
    ok = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="ok")
    error = sgqlc.types.Field(String, graphql_name="error")


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
class CreatePaymentMethodResultType(sgqlc.types.Union):
    __schema__ = schema
    __types__ = (PaymentProfileType, InputErrorType)


class LlmPromptTemplateResultType(sgqlc.types.Union):
    __schema__ = schema
    __types__ = (LlmPromptTemplateType, InputErrorType)


class TrainingDataSourceResultType(sgqlc.types.Union):
    __schema__ = schema
    __types__ = (TrainingDataSourceType, InputErrorType)


class TrainingIndexResultType(sgqlc.types.Union):
    __schema__ = schema
    __types__ = (TrainingIndexType, InputErrorType)


class TrainingItemResultOrErrorType(sgqlc.types.Union):
    __schema__ = schema
    __types__ = (TrainingItemType, InputErrorType)


class UpdateCustomerResultType(sgqlc.types.Union):
    __schema__ = schema
    __types__ = (CustomerType, InputErrorType)


########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = None
