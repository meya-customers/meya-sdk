from meya.time.timedelta import to_timedelta

QUEUE_MAXLEN = 10000
LEDGER_MAXLEN = 200
LEDGER_VIEW_TTL = to_timedelta("3m")
REQUEST_RESPONSE_LEDGER_MAXLEN = 2
