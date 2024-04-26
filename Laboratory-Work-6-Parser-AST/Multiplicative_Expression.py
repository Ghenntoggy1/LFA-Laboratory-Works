from Node import BinaryNode
from Exponential_Expression import Exponential_Expression
from Division_Expression import Division_Expression


class Multiplicative_Expression(BinaryNode):
    @classmethod
    def construct(cls, parser):
        node = Division_Expression.construct(parser)

        if not parser.next().has("*"):
            return node

        op = parser.take()
        right = Multiplicative_Expression.construct(parser)
        return Multiplicative_Expression(node, op, right)
