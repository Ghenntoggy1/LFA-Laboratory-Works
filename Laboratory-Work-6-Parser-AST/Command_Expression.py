from Node import Node
from Variable_Expression import Variable_Expression


class Command_Expression(Node):
    def __init__(self, command, right):
        self.command = command
        self.right = right

    def nodes(self):
        return [self.command, self.right]

    @classmethod
    def construct(cls, parser):
        if parser.next().of("COMMENT_LINE", "COMMENT_BLOCK"):
            return Comment_Expression(parser.take())

        command = Variable_Expression.construct(parser)

        right = parser.expecting_has(";")

        return Command_Expression(command, right)

class Comment_Expression(Node):
    def __init__(self, comment):
        self.comment = comment

    def nodes(self):
        return [self.comment]

    @classmethod
    def construct(cls, parser):
        if parser.next().of("COMMENT_LINE"):
            return Comment_Line_Expression(parser)
        else:
            return Comment_Block_Expression(parser)

class Comment_Block_Expression(Node):
    def __init__(self, comment_line):
        self.comment_line = comment_line

    def nodes(self):
        return [self.comment_line]

    @classmethod
    def construct(cls, parser):
        return Comment_Block_Expression(parser.expecting_of("COMMENT_BLOCK"))

class Comment_Line_Expression(Node):
    def __init__(self, comment_line):
        self.comment_line = comment_line

    def nodes(self):
        return [self.comment_line]

    @classmethod
    def construct(cls, parser):
        return Comment_Line_Expression(parser.expecting_of("COMMENT_LINE"))
