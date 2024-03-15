from Lexer import Lexer
from SourceLine import SourceLine
from Error import LanguageError

import json


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

            json_object = json.dumps(convert(tokens), indent=4)

            with open("./Laboratory-Work-3-Lexer/ExamplePrograms/Tokenized.json", "w") as outfile:
                outfile.write(json_object)
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

            json_object = json.dumps(convert(tokens), indent=4)

            with open("./Laboratory-Work-3-Lexer/ExamplePrograms/Tokenized.json", "w") as outfile:
                outfile.write(json_object)
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

                json_object = json.dumps(convert(tokens), indent=4)

                with open("./Laboratory-Work-3-Lexer/ExamplePrograms/Tokenized.json", "w") as outfile:
                    outfile.write(json_object)
            except LanguageError as error:
                print(error)


def convert(lst):
    res_dict = {}
    for i in range(0, len(lst)):
        print(lst[i])
        key = lst[i].kind
        value = lst[i].string
        if key in res_dict:
            res_dict[key].append(value)
        else:
            res_dict[key] = [value]
    return res_dict


if __name__ == "__main__":
    main()
