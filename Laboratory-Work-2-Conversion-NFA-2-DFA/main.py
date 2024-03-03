# Laboratory Work nr.2
# Student: Gusev Roman
# Group: FAF-222
#
# Variant 11 Grammar:
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
# Variant 11 Finite Automaton:
#     Q = {q0, q1, q2, q3},
#     ∑ = {a, b, c},
#     F = {q3},
#     δ(q0, a) = q1,
#     δ(q1, b) = q2,
#     δ(q2, c) = q0,
#     δ(q1, a) = q3,
#     δ(q0, b) = q2,
#     δ(q2, c) = q3.

import Grammar
import itertools
import FiniteAutomaton
import random

if __name__ == '__main__':
    print("Laboratory Work 2 - Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.")
    print("Variant: 11")
    print("Student: Gusev Roman")
    print("Group: FAF-222")

    # Non-Terminal Terms
    V_n2 = ["q0", "q1", "q2"]
    V_n = ["S", "B", "D", "A"]
    # Terminal Terms
    V_t = ["a", "b", "c"]
    # Rules
    P2 = {
        "q0": ["aq1", "bq1"],
        "q1": ["bq2", "cq1", "aq0"],
        "q2": ["b", "aq2"]
    }
    P = {
        "S": ["aB", "bB"],
        "B": ["bD", "cB", "aS"],
        "D": ["b", "aD"]
    }
    # Start Term
    S2 = "q0"
    S = "S"
    # Maximum Length for generated Words
    max_length = 10

    # -----------------------------HERE STARTS LAB 2--------------------------------------------------------------------

    # Instance of Grammar Class with uppercase notation of Non-Terminal Terms
    grammar = Grammar.Grammar(V_n, V_t, P, S)

    # Check the Grammar type from Laboratory Work 1
    print("Checking Type of Grammar:")
    grammar.check_type_grammar()

    # Instance of Grammar Class with q_ notation of Non-Terminal Terms
    grammar2 = Grammar.Grammar(V_n2, V_t, P2, S2)

    # List that will store all unique Words
    generated_words = []

    # 5 iterations = 5 words
    for i in range(1, 6):
        # Generate a word
        list_of_chars = grammar2.generate_string(max_length)
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
            generated_word = "".join(grammar2.generate_string(max_length))
        # Add the generated word to the list
        generated_words.append(generated_word)
        # Output the Word
        print("\nWord:", i, ": " + "".join(generated_word) + " : Length:", len(generated_word), "\n")

    print("Generated words are: ")
    for word in generated_words:
        print("Word", generated_words.index(word) + 1, ":", word)

    finite_automaton = grammar.to_finite_automaton()
    finite_automaton.print_variables()

    print("\nConverting Finite Automaton to Grammar:", end="")
    grammar_converted = finite_automaton.to_grammar()
    grammar_converted.print_variables()

    print("\nConverting Grammar with q_ notation to Finite Automaton:", end="")
    finite_automaton2 = grammar2.to_finite_automaton()
    finite_automaton2.print_variables()

    print("\nConverting Finite Automaton with q_ notation to Grammar:", end="")
    grammar_converted = finite_automaton2.to_grammar()
    grammar_converted.print_variables()

    # States
    Q = ['q0', 'q1', 'q2']
    # Q = ['q0', 'q1', 'q2', 'q3']

    # Alphabet
    delta = ['a', 'b']
    # delta = ['a', 'b', 'c']

    # Start State
    q0 = 'q0'

    # Final States
    F = ['q2']
    # F = ['q3']

    # Transitions
    sigma = {
        ('q0', 'a'): ['q0', 'q1'],
        ('q0', 'b'): ['q0'],
        ('q1', 'a'): ['q2'],
        ('q2', 'a'): ['q2'],
        ('q2', 'b'): ['q2']
    }

    # sigma = {
    #     ('q0', 'a'): ['q1'],
    #     ('q0', 'b'): ['q2'],
    #     ('q1', 'a'): ['q3'],
    #     ('q1', 'b'): ['q2'],
    #     ('q2', 'c'): ['q0', 'q3']
    # }
    print("\nGiven Finite Automaton:", end="")
    finite_automaton_lab_2 = FiniteAutomaton.FiniteAutomaton(Q, delta, sigma, q0, F)
    finite_automaton_lab_2.print_variables()
    finite_automaton_lab_2.draw_graph("finite_automaton_lab_2")

    print("\nConverted Given Finite Automaton to Regular Grammar:", end="")
    grammar_from_finite_automaton_lab_2 = finite_automaton_lab_2.to_grammar()
    grammar_from_finite_automaton_lab_2.print_variables()

    is_NFA, ambiguous_states = finite_automaton_lab_2.NFA_or_DFA()
    if is_NFA:
        print("Finite Automaton is: Non-Deterministic")
        print("Ambiguous States:")
        for (state, term), next_states in ambiguous_states.items():
            print("\u03C3" + str((state, term)), "-", next_states)
    else:
        print("Finite Automaton is: Deterministic")


    DFA = finite_automaton_lab_2.to_DFA(choice=0)
    DFA.print_variables()
    DFA.draw_graph("DFA1")

    # # Example of Grammars
    # extended_left_regular_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                                 V_t=['a', 'b', 'c'],
    #                                                 P={
    #                                                     'S': ["Aab"],
    #                                                     'A': ["Aab", "B"],
    #                                                     'B': ["a"]
    #                                                 },
    #                                                 S="S")
    # extended_left_regular_grammar.print_variables()
    # extended_left_regular_grammar.check_type_grammar()
    #
    # NFA = extended_left_regular_grammar.to_finite_automaton()
    # is_NFA, ambiguous_states = NFA.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # DFA = NFA.to_DFA(choice=1)
    #
    # extended_right_regular_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                                  V_t=['a', 'b', 'c'],
    #                                                  P={
    #                                                      'S': ["aaA", 'abB', 'aaB'],
    #                                                      'A': ["baA", "B"],
    #                                                      'B': ["a"]
    #                                                  },
    #                                                  S="S")
    # extended_right_regular_grammar.print_variables()
    # extended_right_regular_grammar.check_type_grammar()
    #
    # NFA = extended_right_regular_grammar.to_finite_automaton()
    # is_NFA, ambiguous_states = NFA.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # DFA = NFA.to_DFA(choice=1)
    #
    # left_regular_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                        V_t=['a', 'b', 'c'],
    #                                        P={
    #                                            'S': ["Bb", 'Ac'],
    #                                            'A': ["Sa", "Ac"],
    #                                            'B': ["a"]
    #                                        },
    #                                        S="S")
    # left_regular_grammar.print_variables()
    # left_regular_grammar.check_type_grammar()
    #
    # NFA = left_regular_grammar.to_finite_automaton()
    # is_NFA, ambiguous_states = NFA.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # DFA = NFA.to_DFA(choice=1)
    #
    # right_regular_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                         V_t=['a', 'b', 'c'],
    #                                         P={
    #                                             'S': ["aA", 'bB'],
    #                                             'A': ["bA", "B"],
    #                                             'B': ["a"]
    #                                         },
    #                                         S="S")
    # right_regular_grammar.print_variables()
    # right_regular_grammar.check_type_grammar()
    #
    # NFA = right_regular_grammar.to_finite_automaton()
    # is_NFA, ambiguous_states = NFA.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # DFA = NFA.to_DFA(choice=1)
    #
    # context_free_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                        V_t=['a', 'b', 'c'],
    #                                        P={
    #                                            'S': ["aA", 'bB'],
    #                                            'A': ["BbA", "BA"],
    #                                            'B': ["a"]
    #                                        },
    #                                        S="S")
    # context_free_grammar.print_variables()
    # context_free_grammar.check_type_grammar()
    #
    # context_sensitive_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                             V_t=['a', 'b', 'c'],
    #                                             P={
    #                                                 'S': ["aA", 'bB'],
    #                                                 'AS': ["BbA", "BA"],
    #                                                 'B': ["a"]
    #                                             },
    #                                             S="S")
    # context_sensitive_grammar.print_variables()
    # context_sensitive_grammar.check_type_grammar()
    #
    # unrestricted_grammar = Grammar.Grammar(V_n=['S', 'A', 'B'],
    #                                        V_t=['a', 'b', 'c'],
    #                                        P={
    #                                            'S': ["aA", 'bB'],
    #                                            'AS': ["BbA", "B"],
    #                                            'B': ["a"]
    #                                        },
    #                                        S="S")
    # unrestricted_grammar.print_variables()
    # unrestricted_grammar.check_type_grammar()




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
    # print("\nCHECKING ALL POSSIBLE COMBINATIONS OF TERMINAL TERMS:")
    # possible_words = []
    # for i in range(6):
    #     lst = [''.join(comb) for comb in itertools.product(V_t, repeat=i)]
    #     for word in lst:
    #         possible_words.append(word)
    #
    # for word in possible_words:
    #     result = finite_automaton.string_belong_to_language(word)
    #     print(f"\nWord {word} is {"Accepted" if result else "Rejected"}")
    #
    # # for word in possible_words:
    # #     print(word)
    #
    # finite_automaton.draw_graph("finite_automaton")
    # finite_automaton2.draw_graph("finite_automaton2")

    # finite_automaton = FiniteAutomaton.FiniteAutomaton()
    # finite_automaton.print_variables()
    # # ALL POSSIBLE COMBINATIONS OF WORDS MADE OUT OF TERMINAL TERMS:
    # print("\nCHECKING ALL POSSIBLE COMBINATIONS OF TERMINAL TERMS:")
    # possible_words = []
    # for i in range(6):
    #     lst = [''.join(comb) for comb in itertools.product(V_t, repeat=i)]
    #     for word in lst:
    #         possible_words.append(word)
    #
    # for word in possible_words:
    #     result = finite_automaton.string_belong_to_language(word)
    #     print(f"\nWord {word} is {"Accepted" if result else "Rejected"}")

    # new_grammar = Grammar.Grammar()
    #
    # finite_automaton = grammar.to_finite_automaton()
    # finite_automaton.print_variables()
    #
    # for word in possible_words:
    #     result = finite_automaton.string_belong_to_language(word)
    #     print(f"\nWord {word} is {"Accepted" if result else "Rejected"}")
