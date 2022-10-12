from meya.console.api.schema import Mutation
from meya.console.api.schema import Query
from sgqlc.operation import Operation
from typing import cast


def make_query_op() -> Query:
    return cast(Query, Operation(Query))


def make_mutation_op() -> Mutation:
    return cast(Mutation, Operation(Mutation))
