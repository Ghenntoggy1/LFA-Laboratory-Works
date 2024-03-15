from Error import LanguageError
from Token import Token

class LexerError(LanguageError):
    pass

class Lexer:
    def __init__(self):
        self.line = None

    def new_token(self, kind):
        return Token(kind, self.line)

    def make_tokens(self, line):
        self.line = line
        tokens = []

        while not self.line.finished():
            self.ignore_spaces()
            if self.line.finished():
                break

            tokens += [self.make_token()]

        tokens += [self.new_token("Punctuator")]
        return tokens

    def ignore_spaces(self):
        while self.line.next().isspace():
            self.line.take()
            self.line.ignore()

    def make_token(self):
        if self.line.next() in "()|_^":
            return self.make_punctuator()

        if self.line.next() in "~+-=*/%":
            return self.make_operator()

        if self.line.next() in "0123456789.":
            return self.make_number()

        if self.line.next() == "R":
            return self.make_READFROM()

        self.line.take()
        raise LexerError(self.new_token("?"), "Unrecognized Symbol!")

    def make_punctuator(self):
        self.line.take()
        return self.new_token("Punctuator")

    def make_READFROM(self):
        while self.line.next().isalpha():
            self.line.take()

        if self.line.taken() == "ReadFrom":
            return self.new_token("READFROM")

    def make_operator(self):
        op = self.line.take()

        if op == "*" and self.line.next() == "*":
            self.line.take()

        return self.new_token("Operator")

    def make_number(self):
        while self.line.next() in "0123456789.":
            self.line.take()

        if self.line.taken().count(".") < 2:
            return self.new_token("Number")

        raise LexerError(self.new_token("Number"), "Numbers can have only one decimal point!")
