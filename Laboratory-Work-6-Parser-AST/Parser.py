from Error import LanguageError
from Expression import Expression
from Variable_Expression import Variable_Expression
from Additive_Expression import Additive_Expression
from Command_Expression import Command_Expression

class ParserError(LanguageError):
    pass


class Parser:
    @property
    def expression(self):
        # return Variable_Expression
        return Expression

    @property
    def formula_content(self):
        return Additive_Expression

    def __init__(self):
        self.tokens = None
        self.index = 0

    def next(self):
        return self.tokens[self.index]

    def take(self):
        token = self.next()
        self.index += 1
        return token

    def expecting_has(self, *strings):
        if self.next().has(*strings):
            return self.take()

        raise ParserError(self.next(), f"Expected one of: {strings}")

    def expecting_of(self, *kinds):
        if self.next().of(*kinds):
            return self.take()

        raise ParserError(self.next(), f"Expected one of the type: {kinds}")

    def build_ast(self, tokens):
        self.tokens = tokens
        # node = Variable_Expression.construct(self)
        node = Expression.construct(self)
        if self.next().of("EOF"):
            return node

        raise ParserError(self.next(), f"Unexpected token: {self.next()}")
