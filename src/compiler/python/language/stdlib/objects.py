"""
The tscl objects and data structures.
"""


class Symbol(str):
    pass


class List(list):
    def __repr__(self):
        return '['+' '.join(map(repr, self))+']'


class Map(dict):
    def __repr__(self):
        return '{'+', '.join([' '.join(map(repr, kvp)) for kvp in self.items()])+'}'
