# Laboratory Work nr.1
# Student: Gusev Roman
# Group: FAF-222
#
# Variant 11:
#     VN={S, B, D},
#     VT={a, b, c},
#     P={
#         S → aB
#         S → bB
#         B → bD
#         D → b
#         D → aD
#         B → cB
#         B → aS
#     }

import Grammar
import random

if __name__ == '__main__':
    print("Laboratory Work 1 - Intro to formal languages. Regular grammars. Finite Automata.")
    print("Variant: 11")
    print("Student: Gusev Roman")
    print("Group: FAF-222\n")

    # Non-Terminal Terms
    V_n = ["S", "B", "D"]
    print("Non-Terminal Terms:", V_n, "\n")

    # Terminal Terms
    V_t = ["a", "b", "c"]
    print("Terminal Terms:", V_t, "\n")

    # Rules
    P = {
        "S": ["aB", "bD"],
        "B": ["bD", "cB", "aS"],
        "D": ["b", "aD"]
    }
    print("Rules:")
    for curr_term in P:
        print(curr_term + " -> " + str(P[curr_term]))

    # Start Term
    S = "S"
    print("\nStart Term:", S)

    # Maximum Length for generated Words
    max_length = 10

    # Instance of Grammar Class
    grammar = Grammar.Grammar(V_n, V_t, P, S)

    # List that will store all unique Words
    generated_words = []

    # 5 iterations = 5 words
    for i in range(1, 6):
        # Generate a word
        list_of_chars = grammar.generate_string(max_length)
        if list_of_chars is None:
            exit()
        generated_word = "".join(list_of_chars)
        # Verify if the word is duplicate (is already in the list)
        # or if word length increases maxLength
        # or if last term is Non-Terminal and its derivation is not contained in Rules Dictionary
        while generated_word in generated_words or len(generated_word) > max_length or (
                generated_word[-1] not in P and generated_word[-1].isupper()):
            if generated_word in generated_words:
                print("\nDuplicate: " + "".join(generated_word) +
                      " (Same as Word:", str(generated_words.index(generated_word) + 1) + ")")
            elif generated_word[-1] not in P and generated_word[-1].isupper():
                print("\nNo available further derivation for: " + "".join(generated_word))
            else:
                print("\nWord is too long: " + "".join(generated_word) + " | Length: ", len(generated_word))
            print("Generating new Word...")
            generated_word = "".join(grammar.generate_string(max_length))
        # Add the generated word to the list
        generated_words.append(generated_word)
        # Output the Word
        print("\nWord:", i, ": " + "".join(generated_word) + " : Length:", len(generated_word), "\n")

    print("Generated words are: ")
    for word in generated_words:
        print("Word", generated_words.index(word) + 1, ":", word)

    finite_automaton = grammar.to_finite_automaton()
    finite_automaton.print_variables()

    # Check of method: should be ACCEPTED for all words, because they were generated using this grammar
    for word in generated_words:
        print(
            f"Word {generated_words.index(word) + 1} {word}: {"Accepted" if finite_automaton.string_belong_to_language(word)
            else "Rejected"}"
        )

    # for i in range(10):
    #     input_word = input("\nEnter word: ")
    #     result = finite_automaton.string_belong_to_language(input_word)
    #     print(f"Word {input_word} is {"Accepted" if result else "Rejected"}")
        # Get all the ASCII letters in lowercase and uppercase
    letters = ["a", "b", "c"]

    rejected_words = [
        # Randomly choose characters from letters for the given length of the string
        ''.join(random.choice(letters) for _ in range(3)) for _ in range(50)
    ]
    for word in rejected_words:
        result = finite_automaton.string_belong_to_language(word)
        print(f"Word {word} is {"Accepted" if result else "Rejected"}")

    print(rejected_words)

