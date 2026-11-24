from collections import deque

from . import parsing
from .node import Node
from .notation import prefix_notation
from .notation import simple_notation


class Tree:
    operator_priority = parsing.OPERATOR_PRIORITY
    argument_counts = parsing.ARGUMENT_COUNTS

    def __init__(self):
        self.root = None
        self.stack = deque()

    def set_root(self, node):
        self.root = node

    def validate_formula(self, formula: str) -> None:
        parsing.validate_formula(formula, self.operator_priority, self.argument_counts)

    def validate_postfix(self, formula: str) -> None:
        parsing.validate_postfix(formula, self.argument_counts)

    def is_number(self, part: str) -> bool:
        return parsing.is_number(part)

    def push(self, postfix: str) -> None:
        self.set_root(parsing.parse_postfix(postfix, self.argument_counts))

    def build_from_formula(self, formula: str) -> None:
        parts = parsing.split_formula(formula)
        self.set_root(self.read_expression(parts))

    def read_expression(self, parts: deque[str], min_priority: int = 1) -> Node:
        return parsing.read_expression(
            parts, self.operator_priority, self.argument_counts, min_priority
        )

    def read_operand(self, parts: deque[str]) -> Node:
        return parsing.read_operand(parts, self.operator_priority, self.argument_counts)

    def prefix_notation(self):
        return prefix_notation(self.root)

    def simple_notation(self):
        return simple_notation(self.root)
