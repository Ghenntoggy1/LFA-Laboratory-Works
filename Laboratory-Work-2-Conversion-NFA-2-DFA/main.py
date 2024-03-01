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
import itertools
import FiniteAutomaton
import random

if __name__ == '__main__':
    print("Laboratory Work 1 - Intro to formal languages. Regular grammars. Finite Automata.")
    print("Variant: 11")
    print("Student: Gusev Roman")
    print("Group: FAF-222\n")

    # Non-Terminal Terms
    V_n = ["q0", "q1", "q2"]
    print("Non-Terminal Terms:", V_n, "\n")

    # Terminal Terms
    V_t = ["a", "b", "c"]
    print("Terminal Terms:", V_t, "\n")

    # Rules
    P = {
        "q0": ["aq1", "bq1"],
        "q1": ["bq2", "cq1", "aq0"],
        "q2": ["b", "aq2"]
    }
    print("Rules:")
    for curr_term in P:
        print(curr_term + " -> " + str(P[curr_term]))

    # Start Term
    S = "q0"
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
    # print("\nCHECKING GENERATED WORDS FOR ACCEPTANCE:")
    # for word in generated_words:
    #     print(
    #         f"\nWord {generated_words.index(word) + 1} {word}: {"Accepted" if finite_automaton.string_belong_to_language(word)
    #         else "Rejected"}"
    #     )

    # FOR MANUAL INPUT, UNCOMMENT FOLLOWING LINES OF CODE:
    # iterations = 5
    # for i in range(iterations + 1):
    #     input_word = input("\nEnter word: ")
    #     result = finite_automaton.string_belong_to_language(input_word)
    #     print(f"\nWord {input_word} is {"Accepted" if result else "Rejected"}")

    # FOR RANDOM WORD COMBINATION, UNCOMMENT FOLLOWING LINES OF CODE:
    # length_random = 3
    # number_words = 15
    # random_words = [
    #     # Randomly choose characters from letters for the given length of the string
    #     ''.join(random.choice(V_t) for _ in range(length_random)) for _ in range(number_words)
    # ]
    # for word in random_words:
    #     result = finite_automaton.string_belong_to_language(word)
    #     print(f"\nWord {word} is {"Accepted" if result else "Rejected"}")

    # ALL POSSIBLE COMBINATIONS OF WORDS MADE OUT OF TERMINAL TERMS:
    print("\nCHECKING ALL POSSIBLE COMBINATIONS OF TERMINAL TERMS:")
    possible_words = []
    for i in range(6):
        lst = [''.join(comb) for comb in itertools.product(V_t, repeat=i)]
        for word in lst:
            possible_words.append(word)

    for word in possible_words:
        result = finite_automaton.string_belong_to_language(word)
        print(f"\nWord {word} is {"Accepted" if result else "Rejected"}")

    # for word in possible_words:
    #     print(word)

    finite_automaton.draw_graph()


    finite_automaton = FiniteAutomaton.FiniteAutomaton()
    finite_automaton.print_variables()
    # ALL POSSIBLE COMBINATIONS OF WORDS MADE OUT OF TERMINAL TERMS:
    print("\nCHECKING ALL POSSIBLE COMBINATIONS OF TERMINAL TERMS:")
    possible_words = []
    for i in range(6):
        lst = [''.join(comb) for comb in itertools.product(V_t, repeat=i)]
        for word in lst:
            possible_words.append(word)

    for word in possible_words:
        result = finite_automaton.string_belong_to_language(word)
        print(f"\nWord {word} is {"Accepted" if result else "Rejected"}")
