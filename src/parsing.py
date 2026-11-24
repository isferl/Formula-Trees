from collections import deque
from .node import Node

OPERATOR_PRIORITY = {
    "+": 1, "-": 1,
    "*": 2, "/": 2,
    "^": 3,
}

ARGUMENT_COUNTS = {
    "+": 2,
    "-": 2,
    "*": 2,
    "/": 2,
    "^": 2,
    "sin": 1,
    "cos": 1,
    "tg": 1,
    "ctg": 1,
    "sqrt": 1,
    "ln": 1,
    "log": 2,
    "exp": 1,
}


def split_formula(formula: str) -> deque[str]:
    for symbol in "()+-*/^":
        formula = formula.replace(symbol, f" {symbol} ")
    return deque(formula.split())


def is_number(part: str) -> bool:
    return part.isascii() and part.isdecimal()


def validate_formula(formula: str, operator_priority, argument_counts) -> None:
    parts = split_formula(formula)
    if not parts:
        raise ValueError("Формула пустая")
    expect_operand = True
    open_brackets = []
    while parts:
        part = parts.popleft()
        if expect_operand:
            if part == "x" or is_number(part):
                expect_operand = False
            elif part == "(":
                open_brackets.append(False)
            elif part == "log":
                if not parts or parts[0] != "(":
                    raise ValueError("После 'log' ожидается основание в скобках")
                parts.popleft()
                # После скобок основания должна начаться группа аргумента.
                open_brackets.append(True)
            else:
                is_log = part.startswith("log")
                is_function = (
                        part in argument_counts
                        and part not in operator_priority
                )
                if not (is_function or is_log):
                    raise ValueError(f"Ожидался аргумент, получено {part!r}")
                if is_log and not is_number(part.removeprefix("log")):
                    raise ValueError("Укажи основание логарифма, например log2(x)")
                if not parts or parts[0] != "(":
                    raise ValueError(f"После {part!r} ожидается '('")
        elif part in operator_priority:
            expect_operand = True
        elif part == ")":
            if not open_brackets:
                raise ValueError("Лишняя закрывающая скобка")
            closes_log_base = open_brackets.pop()
            if closes_log_base:
                if not parts or parts[0] != "(":
                    raise ValueError("После основания логарифма ожидается аргумент в скобках")
                expect_operand = True
        else:
            raise ValueError(f"Ожидалась операция или ')', получено {part!r}")
    if expect_operand:
        raise ValueError("Формула заканчивается там, где ожидается аргумент")
    if open_brackets:
        raise ValueError("Не закрыта скобка")


def validate_postfix(formula: str, argument_counts) -> None:
    parts = formula.split()
    if not parts:
        raise ValueError("Формула пустая")
    available = 0
    for part in parts:
        if part == "x" or is_number(part):
            available += 1
            continue
        count = argument_counts.get(part)
        if count is None:
            raise ValueError(f"Неизвестная часть формулы: {part!r}")
        if available < count:
            raise ValueError(f"Для {part!r} не хватает аргументов")
        available = available - count + 1

    if available != 1:
        raise ValueError("Ожидалась одна полная формула")


def parse_postfix(postfix: str, argument_counts) -> Node:
    stack = []
    for token in postfix.split():
        count = argument_counts.get(token)
        if count is None:
            if not (is_number(token) or token == "x"):
                raise ValueError(f"Неизвестный токен: {token!r}")
            stack.append(Node(value=token))
            continue
        if len(stack) < count:
            raise ValueError(f"Для {token!r} не хватает аргументов")
        args = stack[-count:]
        del stack[-count:]
        stack.append(Node(operation=token, args=args))
    if len(stack) != 1:
        raise ValueError("Ожидалась одна полная формула")
    return stack[0]


def read_expression(parts: deque[str], operator_priority, argument_counts, min_priority: int = 1) -> Node:
    left = read_operand(parts, operator_priority, argument_counts)

    while parts and parts[0] in operator_priority:
        operation = parts[0]
        priority = operator_priority[operation]
        if priority < min_priority:
            break

        parts.popleft()

        if operation == "^":
            right_min_priority = priority
        else:
            right_min_priority = priority + 1

        right = read_expression(parts, operator_priority, argument_counts, right_min_priority)
        left = Node(operation=operation, args=[left, right])

    return left


def read_operand(parts: deque[str], operator_priority, argument_counts) -> Node:
    part = parts.popleft()

    if part == "(":
        expression = read_expression(parts, operator_priority, argument_counts)
        parts.popleft()
        return expression

    if part == "log":
        args = []
        for name in ("основание", "аргумент"):
            if not parts or parts[0] != "(":
                raise ValueError(f"Для 'log' ожидается {name} в скобках")
            args.append(read_operand(parts, operator_priority, argument_counts))
        return Node(operation="log", args=args)

    if part.startswith("log"):
        base = Node(value=part.removeprefix("log"))
        argument = read_operand(parts, operator_priority, argument_counts)
        return Node(operation="log", args=[base, argument])

    if part in argument_counts and part not in operator_priority:
        argument = read_operand(parts, operator_priority, argument_counts)
        return Node(operation=part, args=[argument])

    return Node(value=part)
