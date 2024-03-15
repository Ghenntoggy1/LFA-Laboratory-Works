from Lexer import Lexer
from SourceLine import SourceLine
from Error import LanguageError


def main():
    print("Laboratory Work 3 - Lexer")
    print("Student: Gusev Roman")
    print("Group: FAF-222")
    print("\nMY LEXER:")

    lexer = Lexer()
    print("Choose the type of the input:")
    print("F - File")
    print("C - Console all lines together")
    print("L - Console line-by-line")
    while True:
        type_input = input("Your choice: ")
        if type_input.lower() in "lcf":
            break
        else:
            print("Invalid choice!")

    if type_input.lower() == "c":
        lines = ""
        print("Enter lines of code. Type 'exit' to finish.")
        while True:
            line = input("> ")
            if line == "exit":
                break

            lines += line + "\n"

        try:
            source_line = SourceLine(lines)
            tokens = lexer.make_tokens(source_line)

            print("TOKENS:")
            for token in tokens:
                print(token)
        except LanguageError as error:
            print(error)

    elif type_input.lower() == "f":
        with open('./Laboratory-Work-3-Lexer/ExamplePrograms/example_1.txt') as f:
            lines = f.read()

        try:
            source_line = SourceLine(lines)
            tokens = lexer.make_tokens(source_line)

            print("TOKENS:")
            for token in tokens:
                print(token)
        except LanguageError as error:
            print(error)

    elif type_input.lower() == "l":
        print("Enter lines of code. Type 'exit' to finish.")
        while True:
            line = input("> ")
            if line == "exit":
                break

            try:
                source_line = SourceLine(line)
                tokens = lexer.make_tokens(source_line)

                print("TOKENS:")
                for token in tokens:
                    print(token)
            except LanguageError as error:
                print(error)


if __name__ == "__main__":
    main()
