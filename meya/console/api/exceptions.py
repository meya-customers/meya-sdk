class QueryError(Exception):
    def __init__(self, body):
        self.body = body
