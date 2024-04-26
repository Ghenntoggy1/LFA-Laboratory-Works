from Node import BinaryNode
from Unary_Expression import Unary_Expression


class Exponential_Expression(BinaryNode):
    @classmethod
    def construct(cls, parser):
        node = Unary_Expression.construct(parser)

        if not parser.next().has("**"):
            return node

        op = parser.take()
        right = Exponential_Expression.construct(parser)
        return Exponential_Expression(node, op, right)
