from Node import Node
from abc import ABC
from Program_Expression import Program_Expression

class Expression(Node, ABC):
    @classmethod
    def construct(cls, parser):
        return Program_Expression.construct(parser)
