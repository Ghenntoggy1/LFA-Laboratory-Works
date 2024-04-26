from Node import Node, PrimaryNode


class Primary_Expression(Node):
    def __init__(self, left, expression, right):
        self.left = left
        self.expression = expression
        self.right = right

    def nodes(self):
        return [self.left, self.expression, self.right]

    @classmethod
    def construct(cls, parser):
        if not parser.next().has("("):
            if parser.next().of("ID"):
                return Identifier.construct(parser)
            elif parser.next().of("NUMBER"):
                return Number.construct(parser)
            else:
                return IdentifierOrNumber.construct(parser)

        left = parser.take()
        expression = parser.formula_content.construct(parser)
        right = parser.expecting_has(")" if left.has("(") else left.string)

        return Primary_Expression(left, expression, right)


class Number(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return Number(parser.expecting_of("NUMBER"))


class Identifier(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return Identifier(parser.expecting_of("ID"))


class IdentifierOrNumber(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return IdentifierOrNumber(parser.expecting_of("ID", "NUMBER"))