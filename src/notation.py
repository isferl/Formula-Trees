"""Вывод префиксной, постфиксной и скобочной записи (модули 1 и 4–8)."""
from collections import deque
from .node import Node
from .parsing import is_number


def prefix_notation(node: Node):
    if not (node.args):
        return f"{node.value}"
    return f"{node.operation} {" ".join(prefix_notation(i) for i in node.args)}"


def simple_notation(node: Node):
    if not (node.args):
        return f"{node.value}"
    if node.operation in "*-+/^":
        return f"({simple_notation(node.args[0])}{node.operation}{simple_notation(node.args[1])})"
    if node.operation == "log":
        base, argument = node.args
        base_text = simple_notation(base)
        argument_text = simple_notation(argument)

        # Бинарное выражение уже окружено скобками.
        if not is_number(base_text) and not base_text.startswith("("):
            base_text = f"({base_text})"

        return f"log{base_text}({argument_text})"
    return f"{node.operation}({simple_notation(node.args[0])})"
