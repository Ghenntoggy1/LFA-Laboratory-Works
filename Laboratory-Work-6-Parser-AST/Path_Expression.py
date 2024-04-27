from Node import Node


class Path_Expression(Node):
    def __init__(self, expression):
        self.expression = expression

    def nodes(self):
        return [self.expression]

    @classmethod
    def construct(cls, parser):
        expression = parser.expecting_of("PATH")
        return Path_Expression(expression)
