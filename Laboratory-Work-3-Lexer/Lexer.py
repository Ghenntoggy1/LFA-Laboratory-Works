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

        tokens += [self.new_token("EOF")]
        return tokens

    def ignore_spaces(self):
        while self.line.next().isspace():
            self.line.take()
            self.line.ignore()

    def make_token(self):
        if self.line.next() in "()":
            return self.make_parenthesis()

        if self.line.next() == ";":
            return self.make_semicolon()

        if self.line.next() in "<>=":
            return self.make_comparison()

        if self.line.next() in "|_^":
            return self.make_punctuator()

        if self.line.next() in "~+-=%*":
            return self.make_operator()

        if self.line.next() in "0123456789.":
            return self.make_number()

        if self.line.next() in "#":
            return self.make_comment_line()

        if self.line.next() in "/":
            return self.make_comment_block()

        if self.line.next().isalpha() and self.line.next() == "F":
            return self.make_formula()

        if self.line.next().isalpha() and self.line.next() == "D":
            return self.make_data()

        if self.line.next().isalpha():
            return self.make_ID()

        self.line.take()
        raise LexerError(self.new_token("?"), "Unrecognized Symbol!")

    def make_semicolon(self):
        self.line.take()
        return self.new_token("SEMICOLON")

    def make_comparison(self):
        operator = self.line.take()  # Take the first character of the comparison operator

        # Check if the next character is "=" to determine if it's a complete comparison operator
        if self.line.next() == "=":
            operator += self.line.take()  # Take the "=" character
            return self.new_token("COMPARISON_OPERATOR")  # Return the complete comparison operator token

        # If the next character is not "=", treat the standalone character as an assignment operator
        if operator == ">" or operator == "<":
            return self.new_token("COMPARISON_OPERATOR")  # Return the comparison operator token
        else:
            return self.new_token("ASSIGN_OPERATOR")  # Return the assignment operator token

    def make_comment_line(self):
        while not self.line.next() == "\n" and not self.line.finished():
            self.line.take()

        return self.new_token("COMMENT_LINE")

    def make_comment_block(self):
        self.line.take()  # Consume "/"
        if self.line.next() == "*":
            self.line.take()  # Consume "*"
            while True:
                if self.line.next() == "*":
                    self.line.take()  # Consume "*"
                    if self.line.next() == "/":
                        self.line.take()  # Consume "/"
                        return self.new_token("COMMENT_BLOCK")
                elif self.line.finished():
                    raise LexerError(self.new_token("COMMENT_BLOCK"), "Block comment not terminated")
                else:
                    self.line.take()  # Consume non-terminating characters
        else:
            return self.make_operator()


    def make_data(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken() == "Data":
            return self.new_token("DATA")

        raise LexerError(self.new_token("Data"), "Maybe you meant 'Data' instead?")

    def make_formula(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken() == "Formula":
            return self.new_token("FORMULA")

        raise LexerError(self.new_token("Formula"), "Maybe you meant 'Formula' instead?")

    def make_ID(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        return self.new_token("ID")

    # def make_identifier(self):
    #     while self.line.next().isalnum() and not self.line.finished():
    #         self.line.take()
    #
    #     if self.line.taken() == "Formula":
    #         return self.new_token("FORMULA")
    #
    #     if self.line.taken() == "Data":
    #         return self.new_token("DATA")
    #
    #     if self.line.taken() == "ReadFrom":
    #         return self.new_token("READFROM")
    #
    #
    #     raise LexerError(self.new_token("?"), "Unrecognized Symbol!")

    def make_punctuator(self):
        self.line.take()
        return self.new_token("PUNCTUATOR")

    def make_parenthesis(self):
        self.line.take()
        return self.new_token("LPAREN") if "(" in self.line.taken() else self.new_token("RPAREN")

    def make_operator(self):
        op = self.line.take()

        if op == "*" and self.line.next() == "*":
            self.line.take()

        return self.new_token("OPERATOR")

    def make_number(self):
        while self.line.next() in "0123456789.":
            self.line.take()

        if self.line.taken().count(".") < 2:
            return self.new_token("NUMBER")

        raise LexerError(self.new_token("Number"), "Numbers can have only one decimal point!")
