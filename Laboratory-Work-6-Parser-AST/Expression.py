from Node import Node
from Additive_Expression import Additive_Expression
from abc import ABC


class Expression(Node, ABC):
    @classmethod
    def construct(cls, parser):
        return Additive_Expression.construct(parser)
