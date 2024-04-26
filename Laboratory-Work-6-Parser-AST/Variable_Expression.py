from Node import Node
from abc import ABC
from Formula_Expression import Formula_Expression


class Variable_Expression(Node, ABC):
    @classmethod
    def construct(cls, parser):
        return Formula_Expression.construct(parser)
