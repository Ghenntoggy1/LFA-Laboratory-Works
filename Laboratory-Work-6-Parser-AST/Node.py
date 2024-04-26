from abc import ABC, abstractmethod


class Node(ABC):
    @property
    def line(self):
        return self.nodes()[0].line

    @abstractmethod
    def nodes(self):
        pass

    def __repr__(self):
        return self.ast_repr()

    def ast_repr(self, prefix="\t"):
        ast_string = "("
        ast_string += type(self).__name__ + "("
        string = type(self).__name__
        nodes = self.nodes()

        for i, node in enumerate(nodes):
            at_last = (i == len(nodes) - 1)
            symbol = "└── " if at_last else "├── "
            prefix_symbol = "" if at_last else "│"

            node_string = node.ast_repr(f"{prefix}{prefix_symbol}\t")
            string += f"\n{prefix}{symbol} {node_string}"

        ast_string += ")"
        return string

    def mark(self):
        for node in self.nodes():
            node.mark()

    @classmethod
    @abstractmethod
    def construct(cls, parser):
        pass


class PrimaryNode(Node, ABC):
    def __init__(self, token):
        self.token = token

    def nodes(self):
        return [self.token]

    def ast_repr(self, prefix="\t"):
        return f"{self.token.kind} ── {self.token.string}"


class TwoNode(Node, ABC):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def nodes(self):
        return [self.left, self.right]

    @classmethod
    def construct_binary(cls, parser, make, part, ops):
        node = part.construct(parser)

        while parser.next().has(*ops):
            op = parser.take()
            right = part.construct(parser)
            node = make(node, op, right)

        return node


class BinaryNode(Node, ABC):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def nodes(self):
        return [self.left, self.op, self.right]

    @classmethod
    def construct_binary(cls, parser, make, part, ops):
        node = part.construct(parser)

        while parser.next().has(*ops):
            op = parser.take()
            right = part.construct(parser)
            node = make(node, op, right)

        return node


class FourNode(Node, ABC):
    def __init__(self, keyword, identifier, op, right):
        self.keyword = keyword
        self.identifier = identifier
        self.op = op
        self.right = right

    def nodes(self):
        return [self.keyword, self.identifier, self.op, self.right]

    # @classmethod
    # def construct_4Node(cls, parser, keyword, make, part, ops):
    #     node = part.construct(parser)
    #
    #     while parser.next().has(*ops):
    #         op = parser.take()
    #         right = part.construct(parser)
    #         node = make(node, op, right)
    #
    #     return node
    @classmethod
    def construct_binary(cls, parser, make, part, ops):
        node = part.construct(parser)

        while parser.next().has(*ops):
            op = parser.take()
            right = part.construct(parser)
            node = make(node, op, right)

        return node