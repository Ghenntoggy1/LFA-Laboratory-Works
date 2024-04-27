from Node import Node
from Path_Expression import Path_Expression


class Read_From_Path_Expression(Node):
    def __init__(self, keyword, left, path, right):
        self.keyword = keyword
        self.left = left
        self.path = path
        self.right = right

    def nodes(self):
        return [self.keyword, self.left, self.path, self.right]

    @classmethod
    def construct(cls, parser):
        keyword = parser.expecting_of("READ_FROM")
        left = parser.expecting_of("LPAREN")
        path = Path_Expression.construct(parser)
        right = parser.expecting_of("RPAREN")

        return Read_From_Path_Expression(keyword, left, path, right)
