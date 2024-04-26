from Node import Node
from Primary_Expressions import Primary_Expression


class Unary_Expression(Node):
    def __init__(self, op, expression):
        self.op = op
        self.expression = expression

    def nodes(self):
        return [self.op, self.expression]

    @classmethod
    def construct(cls, parser):
        if parser.next().has("+", "-"):
            op = parser.take()
            expression = Unary_Expression.construct(parser)
            return Unary_Expression(op, expression)

        return Primary_Expression.construct(parser)
