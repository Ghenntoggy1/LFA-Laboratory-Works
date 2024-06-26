from Error import LanguageError
from Token import Token
from Tokens import FileType, VariableType, ExportToType, ImageType, PlotType, VisualizationType


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

        if self.line.next() in "[]":
            return self.make_brackets()

        if self.line.next() == ";":
            return self.make_semicolon()

        if self.line.next() == ",":
            return self.make_colon()

        if self.line.next() in "<>=!":
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

        if self.line.next() == '"':
            return self.make_path()

        if self.line.next().isalpha():
            if self.line.next() == "F":
                return self.make_keyword_token("Formula")
            elif self.line.next() == "D":
                return self.make_keyword_token("Data")
            elif self.line.next() == "R":
                return self.make_read_from()
            elif self.line.next() == "E":
                return self.make_export_to()
            elif self.line.next() == "V":
                return self.make_visualization()
            else:
                return self.make_ID()

        self.line.take()
        raise LexerError(self.new_token("?"), "Unrecognized Symbol!")

    def make_visualization(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken() in VisualizationType:
            return self.new_token("VISUALIZATION_TYPE")

        raise LexerError(self.new_token("VISUALIZATION_TYPE"), "Maybe you meant 'VisualData' or 'VisualFormula' instead?")

    def make_brackets(self):
        self.line.take()
        return self.new_token("LBRACKET") if self.line.taken == "[" else self.new_token("RBRACKET")

    def make_path(self):
        self.line.take()  # Consume the starting double quote
        path = ""
        while self.line.next() != '"' and not self.line.finished():
            path += self.line.take()  # Add characters to the path
        if self.line.finished():
            raise LexerError(self.new_token("PATH"), "Path not terminated with double quote")
        self.line.take()  # Consume the ending double quote
        return self.new_token("PATH")

    def make_read_from(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken() == "ReadFrom":
            return self.new_token("READ_FROM")

        raise LexerError(self.new_token("READ_FROM"), "Maybe you meant 'ReadFrom' instead?")

    def make_export_to(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken() in ExportToType:
            return self.new_token("EXPORT_TO_TYPE")

        raise LexerError(self.new_token("EXPORT_TO_TYPE"), "Maybe you meant 'ExportToImage' or 'ExportToFile' instead?")

    def make_semicolon(self):
        self.line.take()
        return self.new_token("SEMICOLON")

    def make_colon(self):
        self.line.take()
        return self.new_token("COLON")

    def make_comparison(self):
        operator = self.line.take()  # Take the first character of the comparison operator

        # Check if the next character is "=" to determine if it's a complete comparison operator
        if self.line.next() == "=":
            operator += self.line.take()
            return self.new_token("COMPARISON_OPERATOR")
        if self.line.next() == "!":
            operator += self.line.take()
            if self.line.next() == "=":
                operator += self.line.take()
                return self.new_token("COMPARISON_OPERATOR")
            raise LexerError(self.new_token("COMPARISON_OPERATOR"), "Invalid comparison operator")
        # If the next character is not "=", treat the standalone character as an assignment operator
        if operator == ">" or operator == "<":
            return self.new_token("COMPARISON_OPERATOR")
        else:
            return self.new_token("ASSIGN_OPERATOR")

    def make_comment_line(self):
        while not self.line.next() == "\n" and not self.line.finished():
            self.line.take()
        return self.new_token("COMMENT_LINE")

    def make_comment_block(self):
        self.line.take()
        if self.line.next() == "*":
            self.line.take()
            while True:
                if self.line.next() == "*":
                    self.line.take()
                    if self.line.next() == "/":
                        self.line.take()
                        return self.new_token("COMMENT_BLOCK")
                elif self.line.finished():
                    raise LexerError(self.new_token("COMMENT_BLOCK"), "Block comment not terminated")
                else:
                    self.line.take()
        else:
            return self.make_operator()

    def make_keyword_token(self, keyword_type):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken() in VariableType:
            return self.new_token("VARIABLE_TYPE")
        elif self.line.taken() in ExportToType:
            return self.new_token("EXPORT_TO_TYPE")

        raise LexerError(self.new_token("VARIABLE_TYPE"), f"Maybe you meant '{keyword_type}' instead?")

    def make_ID(self):
        while self.line.next().isalnum() and not self.line.finished():
            self.line.take()

        if self.line.taken().lower() in FileType:
            return self.new_token("FILE_TYPE")

        if self.line.taken().lower() in ImageType:
            return self.new_token("IMAGE_TYPE")

        if self.line.taken().lower() in PlotType:
            return self.new_token("PLOT_TYPE")

        if self.line.taken() in VariableType:
            return self.new_token("VARIABLE_TYPE")

        if self.line.taken() == "range":
            return self.new_token("RANGE")

        return self.new_token("ID")

    def make_punctuator(self):
        self.line.take()
        return self.new_token("PUNCTUATOR")

    def make_parenthesis(self):
        self.line.take()
        return self.new_token("LPAREN") if "(" in self.line.taken() else self.new_token("RPAREN")

    def make_operator(self):
        if self.line.taken() == "/":
            if self.line.next() == "/":
                self.line.take()
            return self.new_token("OPERATOR")
        op = self.line.take()
        if op == "*" and self.line.next() == "*":
            self.line.take()

        return self.new_token("OPERATOR")

    def make_number(self):
        while self.line.next() in "0123456789.":
            self.line.take()

        if self.line.taken().count(".") == 1 and len(self.line.taken()) == 1:
            return self.new_token("DOT")
        if self.line.taken().count(".") < 2:
            return self.new_token("NUMBER")
        raise LexerError(self.new_token("Number"), "Numbers can have only one decimal point!")
