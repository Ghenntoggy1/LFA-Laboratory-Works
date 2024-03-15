from Lexer import Lexer
from SourceLine import SourceLine
from Error import LanguageError


def main():
    print("Laboratory Work 3 - Lexer")
    print("Student: Gusev Roman")
    print("Group: FAF-222")
    print("\nMY LEXER:")

    lexer = Lexer()

    while True:
        line = input("> ")
        if line == "exit":
            break

        try:
            line = SourceLine(line)
            tokens = lexer.make_tokens(line)
            print(tokens)
        except LanguageError as error:
            print(error)


if __name__ == "__main__":
    main()
