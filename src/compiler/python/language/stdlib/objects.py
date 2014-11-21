"""
The tscl objects and data structures.
"""


class Boolean:
    def __init__(self, value):
        self.value = bool(value)

    def __bool__(self):
        return self.value

    # todo: lots more magic methods to define ...

    def __repr__(self):
        return 'true' if self.value else 'false'


class Symbol(str):
    pass


class List(list):
    def __repr__(self):
        return '['+' '.join(map(repr, self))+']'


class Map(dict):
    def __repr__(self):
        return '{'+', '.join([' '.join(map(repr, kvp)) for kvp in self.items()])+'}'
