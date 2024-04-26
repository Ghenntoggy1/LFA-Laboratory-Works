from Node import Node
from abc import ABC
from Formula_Expression import Variable_Expression
from Additive_Expression import Additive_Expression


class Expression(Node, ABC):
    @classmethod
    def construct(cls, parser):
        # if parser.next().of("VARIABLE_TYPE"):
        return Variable_Expression.construct(parser)
        # else:
        # return Additive_Expression.construct(parser)