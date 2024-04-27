from Lexer import Lexer
from SourceLine import SourceLine
from Error import LanguageError
from Parser import Parser

import json
import tkinter as tk
from tkinter import filedialog
import os


def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(initialdir="./Laboratory-Work-6-Parser-AST/ExamplePrograms",
                                           title="Select a file")

    return file_path


def main():
    print("Laboratory Work 6 - Parser and AST")
    print("Student: Gusev Roman")
    print("Group: FAF-222")
    print("\nMY LEXER AND PARSER:")

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

    print("")
    if type_input.lower() == "c":
        lines = ""
        print("Enter lines of code. Type 'exit' to finish.")
        while True:
            line = input("> ")
            if line == "exit":
                break
            if line == "":
                continue
            lines += line + "\n"

        try:
            source_line = SourceLine(lines)
            tokens = lexer.make_tokens(source_line)

            parser = Parser()
            tree = parser.build_ast(tokens)
            print("TOKENS:")
            for token in tokens:
                print(token)

            print("AST:")
            print(tree.ast_repr())
            json_object = json.dumps(convert(tokens), indent=4)

            with open("./Laboratory-Work-6-Parser-AST/ExamplePrograms/Tokenized_Manual_Input.json", "w") as outfile:
                outfile.write(json_object)
        except LanguageError as error:
            print(error)

    elif type_input.lower() == "f":
        file_path = select_file()

        if not file_path:
            print("No file selected.")
            return

        with open(file_path) as f:
            lines = f.read()

        try:
            source_line = SourceLine(lines)
            tokens = lexer.make_tokens(source_line)

            parser = Parser()
            tree = parser.build_ast(tokens)
            print("TOKENS:")
            for token in tokens:
                print(token)

            print("AST:")
            print(tree.ast_repr())
            json_object = json.dumps(convert(tokens), indent=4)

            with open(
                    f"./Laboratory-Work-6-Parser-AST/ExamplePrograms/Tokenized_{os.path.splitext(os.path.basename(file_path))[0]}.json",
                    "w") as outfile:
                outfile.write(json_object)
        except LanguageError as error:
            print(error)

    elif type_input.lower() == "l":
        print("Enter lines of code. Type 'exit' to finish.")
        while True:
            line = input("> ")
            if line == "exit":
                break
            if line == "":
                continue
            try:
                source_line = SourceLine(line)
                tokens = lexer.make_tokens(source_line)
                parser = Parser()
                tree = parser.build_ast(tokens)
                print("TOKENS:")
                for token in tokens:
                    print(token)

                print("AST:")
                print(tree.ast_repr())
                json_object = json.dumps(convert(tokens), indent=4)

                with open("./Laboratory-Work-6-Parser-AST/ExamplePrograms/Tokenized_Manual_Input.json", "w") as outfile:
                    outfile.write(json_object)
            except LanguageError as error:
                print(error)


def convert(lst):
    res_dict = {}
    for i in range(0, len(lst)):
        key = lst[i].kind
        value = lst[i].string
        locale = lst[i].locale
        if key in res_dict:
            res_dict[key].update({value: locale})
        else:
            res_dict[key] = {value: locale}
    return res_dict


if __name__ == "__main__":
    main()
