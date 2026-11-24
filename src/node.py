class Node:
    def __init__(self, value=None, operation=None, args=()):
        self.value = value
        self.operation = operation
        self.args = list(args)
