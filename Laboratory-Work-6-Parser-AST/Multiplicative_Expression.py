from Node import BinaryNode
from Exponential_Expression import Exponential_Expression


class Multiplicative_Expression(BinaryNode):
    @classmethod
    def construct(cls, parser):
        return cls.construct_binary(parser, cls, Exponential_Expression, ["*", "/"])
