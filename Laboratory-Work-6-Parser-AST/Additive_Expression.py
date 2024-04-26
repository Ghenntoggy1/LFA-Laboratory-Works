from Node import BinaryNode
from Multiplicative_Expression import Multiplicative_Expression


class Additive_Expression(BinaryNode):
    @classmethod
    def construct(cls, parser):
        return cls.construct_binary(parser, cls, Multiplicative_Expression, ["+", "-"])
