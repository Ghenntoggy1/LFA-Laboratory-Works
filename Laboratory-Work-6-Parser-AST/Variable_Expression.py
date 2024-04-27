from Node import Node, PrimaryNode
from Primary_Expressions import Identifier
from Additive_Expression import Additive_Expression
from Read_From_Path_Expression import Read_From_Path_Expression

class Variable_Expression(Node):
    def __init__(self, keyword, identifier, op, expression):
        self.keyword = keyword
        self.identifier = identifier
        self.op = op
        self.expression = expression

    def nodes(self):
        return [self.keyword, self.identifier, self.op, self.expression]

    @classmethod
    def construct(cls, parser):
        # Expect 'Formula' or 'Data' keyword
        keyword = parser.expecting_has("Formula", "Data")

        # Expect Identifier (ID)
        identifier = Identifier.construct(parser)

        # Expect '=' symbol
        op = parser.expecting_has("=")

        # Parse Expression
        if keyword.has("Formula"):
            expression = Additive_Expression.construct(parser)
        else:
            expression = Read_From_Path_Expression.construct(parser)

        return Variable_Expression(keyword, identifier, op, expression)


class Formula(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return Formula(parser.expecting_has("Formula"))


class Data(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return Data(parser.expecting_has("Data"))


class FormulaOrData(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return FormulaOrData(parser.expecting_has("Formula", "Data"))
