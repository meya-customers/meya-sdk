from meya.time.timedelta import to_timedelta

SENSITIVE_DATA_TTL = to_timedelta("1h")
SENSITIVE_EVENT_TTL = to_timedelta("24h")
SENSITIVE_MEDIA_TTL = to_timedelta("30d")
