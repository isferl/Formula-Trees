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
        "sqrt": 1,
        "ln": 1,
        "log": 2,
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
            is_number = data and all("0" <= char <= "9" for char in data)
            is_variable = len(data) == 1 and data.isalpha()
            if not (is_number or is_variable):
                raise ValueError(f"Неизвестное значение: {data!r}")
            self.stack.append(Node(value=data))
            return

        if len(self.stack) < count:
            raise ValueError(f"Для {data!r} не хватает аргументов")

        args = tuple(self.stack[-count:])
        del self.stack[-count:]
        self.stack.append(Node(operation=data, args=args))
