class Node:
    def __init__(self, value=None, operation=None, args=()):
        self.value = value
        self.operation = operation
        self.args = args


class Tree:
    argument_counts = {
        "+": 2,
        "-": 2,
        "*": 2,
        "/": 2,
        "^": 2,
        "sin": 1,
        "cos": 1,
        "tg": 1,
        "ctg": 1,
        "tan": 1,
        "cot": 1,
        "sqrt": 1,
        "ln": 1,
        "log": 1,
        "exp": 1,
    }

    def __init__(self):
        self.root = None
        self.stack = []

    def set_root(self, node):
        self.root = node

    def push(self, data: str):
        count = self.argument_counts.get(data)

        if count is None:
            if not (data.isdecimal() or data.isidentifier()):
                raise ValueError(f"Неизвестный токен: {data!r}")

            self.stack.append(Node(value=data))
            return

        if len(self.stack) < count:
            raise ValueError(f"Для {data!r} не хватает аргументов")

        args = tuple(self.stack[-count:])
        del self.stack[-count:]
        self.stack.append(Node(operation=data, args=args))
