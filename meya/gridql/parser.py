import luqum.parser
import ply.yacc as yacc
import pytz
import re

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from dateutil import parser as date_parser
from luqum.parser import Fuzzy
from luqum.parser import Item
from luqum.parser import Phrase
from luqum.parser import SearchField
from luqum.parser import Term
from luqum.parser import UnknownOperation
from luqum.parser import Word
from luqum.tree import AndOperation
from luqum.tree import FieldGroup
from luqum.tree import Group
from luqum.tree import Not
from luqum.tree import OrOperation
from luqum.tree import Range
from luqum.tree import Regex
from meya.core.abstract_type_registry import AbstractTypeRegistry
from meya.entry import Entry
from meya.time.time import from_utc_milliseconds_timestamp
from meya.util.json import to_json
from numbers import Real
from ply.lex import LexToken
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import cast

# `yacc.get_caller_module_dict` uses reflection to configure the yacc parser so
# we reset luqum yacc globals here to override the p_error implementation in
# luqum.
reserved = luqum.parser.reserved
tokens = luqum.parser.tokens
t_PLUS = luqum.parser.t_PLUS
t_MINUS = luqum.parser.t_MINUS
t_NOT = luqum.parser.t_NOT
t_AND_OP = luqum.parser.t_AND_OP
t_OR_OP = luqum.parser.t_OR_OP
t_COLUMN = luqum.parser.t_COLUMN
t_LPAREN = luqum.parser.t_LPAREN
t_RPAREN = luqum.parser.t_RPAREN
t_LBRACKET = luqum.parser.t_LBRACKET
t_RBRACKET = luqum.parser.t_RBRACKET
precedence = luqum.parser.precedence
TIME_RE = luqum.parser.TIME_RE
TERM_RE = luqum.parser.TERM_RE
PHRASE_RE = luqum.parser.PHRASE_RE
APPROX_RE = luqum.parser.APPROX_RE
REGEX_RE = luqum.parser.REGEX_RE
t_SEPARATOR = luqum.parser.t_SEPARATOR
t_TERM = luqum.parser.t_TERM
t_PHRASE = luqum.parser.t_PHRASE
t_REGEX = luqum.parser.t_REGEX
t_APPROX = luqum.parser.t_APPROX
t_BOOST = luqum.parser.t_BOOST
t_error = luqum.parser.t_error
lexer = luqum.parser.lexer
p_expression_or = luqum.parser.p_expression_or
p_expression_and = luqum.parser.p_expression_and
p_expression_implicit = luqum.parser.p_expression_implicit
p_expression_plus = luqum.parser.p_expression_plus
p_expression_minus = luqum.parser.p_expression_minus
p_expression_not = luqum.parser.p_expression_not
p_expression_unary = luqum.parser.p_expression_unary
p_grouping = luqum.parser.p_grouping
p_range = luqum.parser.p_range
p_field_search = luqum.parser.p_field_search
p_quoting = luqum.parser.p_quoting
p_proximity = luqum.parser.p_proximity
p_boosting = luqum.parser.p_boosting
p_terms = luqum.parser.p_terms
p_fuzzy = luqum.parser.p_fuzzy
p_regex = luqum.parser.p_regex
p_to_as_term = luqum.parser.p_to_as_term
p_phrase_or_term = luqum.parser.p_phrase_or_term


class QueryException(Exception):
    """
    Exception raised when parsing a query string fails
    """

    pass


def p_error(token: LexToken):
    if token is None:
        raise QueryException(
            "Unexpectedly reached the end of the query, this is possibly due "
            "to an unmatched parenthesis."
        )
    if hasattr(token, "value"):
        value = token.value
        if isinstance(token.value, Term):
            value = token.value.value
        special_chars = '+-=&|><!(){}[]^"~*?:\/@'
        error_message = f"Query syntax error at '{value}' in position {cast(Any, token).lexpos}."
        if value in special_chars:
            error_message += (
                f"The value '{value}' is one of the special characters '{special_chars}', "
                f"if you would like to include '{value}' as a literal you can escape "
                f"it with '\\'. Note, for date times you need to quote the date time "
                f'string e.g. "2020-09-10T12:00:00.500Z".'
            )
        raise QueryException(error_message)
    else:
        raise QueryException(
            f"Query syntax error at position {cast(Any, token).lexpos}."
        )


gridql_parser = yacc.yacc()


@dataclass
class GridQL:
    tree: Item = field()
    type_registry: Optional[AbstractTypeRegistry] = field(default=None)
    entry: Optional[Entry] = field(default=None, init=False)
    timestamp: Optional[datetime] = field(default=None, init=False)
    match_operations: Dict[Type[Item], Callable] = field(init=False)
    MAX_DEPTH: ClassVar[int] = 10
    TYPE_FIELD: ClassVar[str] = "type"
    TIMESTAMP_FIELD: ClassVar[str] = "timestamp"

    def __post_init__(self):
        # This dictionary maps supported luqum classes to methods on this class
        self.match_operations = {
            Group: self._match_group,
            FieldGroup: self._match_group,
            Not: self._match_not,
            AndOperation: self._match_and,
            UnknownOperation: self._match_and,
            OrOperation: self._match_or,
            SearchField: self._match_search_field,
            Word: self._match_term,
            Phrase: self._match_term,
            Regex: self._match_term,
            Range: self._match_range_field,
        }
        # Raise a QueryException if the user has passed unsupported search terms
        self._check_tree(self.tree)

    @classmethod
    def create(
        cls,
        query: Optional[str],
        type_registry: Optional[AbstractTypeRegistry] = None,
    ) -> "GridQL":
        """
        Factory method for creating a GridQL object

        query: A Lucene style query
        """
        return cls(cls.parse(query), type_registry=type_registry)

    @classmethod
    def parse(cls, query: Optional[str]) -> Item:
        """
        query: A Lucene style query string
        """
        if query is None or not query.strip():
            tree = UnknownOperation()
        else:
            tree = gridql_parser.parse(query)
        return tree

    def _check_tree(self, item: Item, depth: int = 0) -> None:
        """Check for unsupported object types in the tree

        Args:
            item: The tree item to check.
            depth: Current recursion depth, used to avoid infinite loops or
                   malicious queries.

        Raises:
            QueryException: If a query is invalid, by being too complicated or
            containing unsupported features.
        """
        depth += 1
        if depth > self.MAX_DEPTH:
            raise QueryException(
                "Query too complicated, increase max_depth if required"
            )

        elif isinstance(item, Fuzzy):
            raise QueryException(
                "Fuzzy matching with ~ is not currently supported"
            )

        elif not any(
            isinstance(item, t) for t in self.match_operations.keys()
        ):
            raise QueryException(
                f"Unsupported operation type {type(item).__name__} {str(item)}"
            )

        if isinstance(item, (SearchField, Not, Group, FieldGroup)):
            if len(item.children) == 0:
                raise QueryException(
                    f"Unhandled  type {type(item).__name__} {str(item)} with no children"
                )
            elif len(item.children) > 1:
                raise QueryException(
                    f"Unhandled  type {type(item).__name__} {str(item)} with more than 1 child"
                )

        for child in item.children:
            self._check_tree(child, depth=depth)

    def match(self, data: dict) -> bool:
        return self._match(data, self.tree, scope_field=None)

    def match_entry(self, entry: Entry) -> bool:
        assert (
            self.type_registry is not None
        ), "`type_registry` must be specified for entry matching"

        try:
            self.entry = entry
            if self.entry.entry_id:
                self.timestamp, _ = entry.entry_timestamp_and_seq
            else:
                self.timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)
            return self.match(self.entry.to_dict())
        finally:
            self.entry = None
            self.timestamp = None

    def _match(
        self, data: dict, operation: Item, scope_field: Optional[str]
    ) -> bool:
        """
        Internal method that recurses through the query AST to conduct matching.

        Args:
            data: A dictionary containing fields and values to match against.
            operation: The current luqum.tree object which is being matched.

        Returns:
            True if the match succeeds, False otherwise.
        """
        # TODO: Add query compile phase to process AST that converts all
        #       search/range field values to specific matcher e.g. compiled
        #       regex object. _match should only match against concrete
        #       matcher objects.
        handler = self.match_operations[type(operation)]
        return handler(data, operation, scope_field)

    def _match_group(
        self, data: dict, operation: Group, scope_field: Optional[str]
    ) -> bool:
        return self._match(data, operation.children[0], scope_field)

    def _match_not(
        self, data: dict, operation: Not, scope_field: Optional[str]
    ) -> bool:
        return not self._match(data, operation.children[0], scope_field)

    def _match_and(
        self, data: dict, operation: AndOperation, scope_field: Optional[str]
    ) -> bool:
        for child in operation.children:
            if not self._match(data, child, scope_field):
                return False
        return True

    def _match_or(
        self, data: dict, operation: OrOperation, scope_field: Optional[str]
    ) -> bool:
        for child in operation.children:
            if self._match(data, child, scope_field):
                return True
        return False

    def _match_search_field(
        self, data: dict, operation: SearchField, scope_field: Optional[str]
    ) -> bool:
        return self._match(
            data,
            operation.children[0],
            scope_field=self._extend_scope_field(operation, scope_field),
        )

    def _extend_scope_field(
        self, operation: SearchField, scope_field: Optional[str]
    ):
        return (
            operation.name
            if not scope_field
            else f"{scope_field}.{operation.name}"
        )

    def _match_term(
        self,
        data: dict,
        operation: Union[Word, Phrase],
        scope_field: Optional[str],
    ) -> bool:
        if (
            scope_field is None or scope_field == self.TYPE_FIELD
        ) and self.is_entry_search:
            return self._match_term_entry_type(operation)

        elif not scope_field:
            return False

        try:
            value = self._get_value(data, scope_field)
        except (KeyError, TypeError):
            return False

        pattern = re.compile(self._get_term_pattern(operation))
        for expanded_value in value if isinstance(value, list) else [value]:
            if isinstance(expanded_value, (bool, Real)):
                # Allow matching some basic string-compatible types
                expanded_value = to_json(expanded_value)

            elif isinstance(expanded_value, str):
                pass

            else:
                # Don't allow matching any other types
                continue

            if re.match(pattern, expanded_value):
                return True

        return False

    def _match_term_entry_type(self, operation: Union[Word, Phrase]) -> bool:
        entry_type = self._unescape_term(operation)
        try:
            entry_class = Entry.get_entry_type_subclass(
                entry_type, type_registry=self.type_registry
            )
        except:
            raise QueryException(
                f"Invalid reference to entry type `{entry_type}`"
            )
        return isinstance(self.entry, entry_class)

    def _match_range_field(
        self, data: dict, operation: Range, scope_field: Optional[str]
    ) -> bool:
        if not scope_field and self.is_entry_search:
            scope_field = self.TIMESTAMP_FIELD
        if not scope_field:
            return False
        if scope_field == self.TIMESTAMP_FIELD and self.is_entry_search:
            range_tuple = self._parse_datetime_range_values(operation)
            value = self.timestamp
        else:
            range_tuple = self._parse_float_range_values(operation)
            try:
                value = self._get_value(data, scope_field)
            except (KeyError, TypeError):
                return False
        low, high, include_low, include_high = range_tuple

        for expanded_value in value if isinstance(value, list) else [value]:
            try:
                if include_low:
                    greater_than = expanded_value >= low
                else:
                    greater_than = expanded_value > low
                if include_high:
                    less_than = expanded_value <= high
                else:
                    less_than = expanded_value < high
            except TypeError:
                continue
            if greater_than and less_than:
                return True

        return False

    def _parse_datetime_range_values(
        self, operation: Range
    ) -> Tuple[datetime, datetime, bool, bool]:
        low = self._parse_datetime_value(operation.low)
        high = self._parse_datetime_value(operation.high)
        if low > high:
            raise QueryException(
                f"Incorrect range specified, '{low}' must be less than '{high}'."
            )
        return low, high, operation.include_low, operation.include_high

    def _parse_float_range_values(
        self, operation: Range
    ) -> Tuple[float, float, bool, bool]:
        low = self._parse_float_value(operation.low)
        high = self._parse_float_value(operation.high)
        if low > high:
            raise QueryException(
                f"Incorrect range specified, '{low}' must be less than '{high}'."
            )
        return low, high, operation.include_low, operation.include_high

    def _parse_datetime_value(self, item: Item) -> datetime:
        value = self._unescape_term(item)
        try:
            return date_parser.parse(value).astimezone(pytz.utc)
        except (TypeError, ValueError, OverflowError):
            pass

        try:
            return from_utc_milliseconds_timestamp(int(value))
        except (TypeError, ValueError):
            raise QueryException(
                f"Could not convert '{value}' to a date time value."
            )

    def _parse_float_value(self, item: Item) -> float:
        value = self._unescape_term(item)
        try:
            return float(value)
        except ValueError:
            raise QueryException(
                f"Could not convert '{value}' to a number value."
            )

    @property
    def is_entry_search(self) -> bool:
        return bool(self.type_registry and self.entry)

    @staticmethod
    def _unescape_term(operation: Item) -> str:
        if isinstance(operation, Phrase):
            operation = Word(operation.value[1:-1])

        if isinstance(operation, Word):
            if operation.has_wildcard():
                raise QueryException(
                    f"Invalid operation {operation}. Wildcard not supported here."
                )

            return operation.unescaped_value

        raise QueryException(
            f"Invalid operation {operation}. Must be Word or Phrase."
        )

    @staticmethod
    def _get_value(data: dict, key: str):
        for expanded_key in key.split("."):
            data = data[expanded_key]
        return data

    @staticmethod
    def _get_term_pattern(operation: Item) -> str:
        if isinstance(operation, Regex):
            return f"^{operation.value[1:-1]}$"

        if isinstance(operation, Phrase):
            operation = Word(operation.value[1:-1])

        if isinstance(operation, Word):
            parts = operation.split_wildcards()
            pattern = ""
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    pattern += re.escape(Word(part).unescaped_value)
                elif part == "*":
                    pattern += ".*"
                elif part == "?":
                    pattern += "."
                else:
                    raise QueryException(
                        f"Invalid wildcard {part} in operation {operation}."
                    )
            return f"^{pattern}$"

        raise QueryException(
            f"Invalid operation {operation}. Must be Word or Phrase."
        )

    def _search_entry_type(self, entry_type: str):
        # check if the entry is an instance/subclass of the provided entry type
        try:
            entry_class = Entry.get_entry_type_subclass(
                entry_type, type_registry=self.type_registry
            )
        except:
            raise QueryException(
                f"Invalid reference to entry type `{entry_type}`"
            )

        return isinstance(self.entry, entry_class)
