# Laboratory Work nr.5
# Student: Gusev Roman
# Group: FAF-222
#
# Variant 11 Grammar:
#     VN={S, A, B, C, D},
#     VT={a, b},
#     P={
#         S → bA
#         S → AC
#         A → bS
#         A → BC
#         A → AbAa
#         B → BbaA
#         B → a
#         B → bSa
#         C → ε
#         D → AB
#     }

import Grammar
import itertools
# import FiniteAutomaton
import random

if __name__ == '__main__':
    print("Laboratory Work 5 - Chomsky Normal Form.")
    print("Variant: 11")
    print("Student: Gusev Roman")
    print("Group: FAF-222")

    # Non-Terminal Terms
    V_n = {"S", "A", "B", "D", "C"}
    # V_n = {"S", "X", "Y", "Z"}

    # Terminal Terms
    V_t = {"a", "b"}
    # V_t = {"0", "1"}

    # P = {
    #     "S": {"XYX", "XY", "YX", "1Y", "1", "XX", "0X", "0"},
    #     "X": {"0X", "0"},
    #     "Y": {"1Y", "1"},
    #     "Z": {"1Y", "1"}
    # }

    P = {
        "S": {"bA", "AC"},
        "A": {"bS", "BC", "AbAa"},
        "B": {"BbaA", "a", "bSa"},
        "C": {"epsilon"},
        "D": {"AB"}
    }

    # P = {
    #         "S": {"bA", "ACAC"},
    #         "A": {"bS", "BC", "AbAa"},
    #         "B": {"BbaA", "a", "bSa"},
    #         "C": {"epsilon", "a", "aC"},
    #         "D": {"AB"}
    #     }

    # P = {
    #     "S": {"AaD", "a"},
    #     "B": {"C"},
    #     "A": {"Bb"},
    #     "D": {"b"},
    #     "C": {"aA"}
    # }

    # P = {
    #     "S": {"dB", "AB"},
    #     "A": {"d", "dS", "aAaAb", "epsilon"},
    #     "B": {"a", "aS", "A"},
    #     "D": {"Aba"}
    # }
    #
    # Start Term
    S = "S"

    # # Maximum Length for generated Words
    # max_length = 10

    # -----------------------------HERE STARTS LAB 5--------------------------------------------------------------------

    # Instance of Grammar Class with uppercase notation of Non-Terminal Terms
    print("\nGenerating Grammar from Input from Laboratory Work 5...")
    grammar = Grammar.Grammar(V_n, V_t, P, S)

    print("Printing Grammar from Input from Laboratory Work 5:", end="")
    grammar.print_variables()

    # Check the Grammar type from Laboratory Work 5
    print("Checking Type of Grammar:")
    grammar.check_type_grammar()

    CNF_Grammar = grammar.convert_to_Chomsky_Normal_Form()

    # # Instance of Grammar Class with q_ notation of Non-Terminal Terms
    # print("\nGenerating Grammar from Input from Laboratory Work 1 with q_ notation...")
    # grammar2 = Grammar.Grammar(V_n2, V_t, P2, S2)
    #
    # print("Printing Grammar from Input from Laboratory Work 1 with q_ notation:", end="")
    # grammar2.print_variables()

    # print("\nGenerating words using given Grammar:")
    # # List that will store all unique Words
    # generated_words = []

    # # 5 iterations = 5 words
    # for i in range(1, 6):
    #     # Generate a word
    #     list_of_chars = grammar.generate_string(max_length)
    #     if list_of_chars is None:
    #         exit()
    #     generated_word = "".join(list_of_chars)
    #     # Verify if the word is duplicate (is already in the list)
    #     # or if word length increases maxLength
    #     # or if last term is Non-Terminal and its derivation is not contained in Rules Dictionary
    #     while generated_word in generated_words or len(generated_word) > max_length or (
    #             generated_word[-1] not in P and generated_word[-1].isupper()):
    #         if generated_word in generated_words:
    #             print("\nDuplicate: " + "".join(generated_word) +
    #                   " (Same as Word:", str(generated_words.index(generated_word) + 1) + ")")
    #         elif generated_word[-1] not in P and generated_word[-1].isupper():
    #             print("\nNo available further derivation for: " + "".join(generated_word))
    #         else:
    #             print("\nWord is too long: " + "".join(generated_word) + " | Length: ", len(generated_word))
    #         print("Generating new Word...")
    #         generated_word = "".join(grammar.generate_string(max_length))
    #     # Add the generated word to the list
    #     generated_words.append(generated_word)
    #     # Output the Word
    #     print("\nWord:", i, ": " + "".join(generated_word) + " : Length:", len(generated_word), "\n")
    #
    # print("Generated words are: ")
    # for word in generated_words:
    #     print("Word", generated_words.index(word) + 1, ":", word)
    #
    # print("\nConverting Given Grammar from Laboratory Work 1 to Finite Automaton...")
    # finite_automaton = grammar.to_finite_automaton()
    #
    # print("Generated Finite Automaton:")
    # finite_automaton.print_variables()
    #
    # print("\nConverting Finite Automaton to Grammar:")
    # choice = 1
    # if input("Add final state to Grammar? (Y/N): ").lower() == "n":
    #     choice = 0
    # grammar_converted = finite_automaton.to_grammar(choice)
    # grammar_converted.print_variables()
    #
    # print("\nConverting Grammar with q_ notation to Finite Automaton:", end="")
    # finite_automaton2 = grammar2.to_finite_automaton()
    # finite_automaton2.print_variables()
    #
    # print("\nConverting Finite Automaton with q_ notation to Grammar:")
    # choice = 1
    # if input("Add final state to Grammar? (Y/N): ").lower() == "n":
    #     choice = 0
    # grammar_converted = finite_automaton2.to_grammar(choice)
    # grammar_converted.print_variables()

    # # States
    # # Q = ['q0', 'q1', 'q2']
    # Q = ['q0', 'q1', 'q2', 'q3']
    #
    # # Alphabet
    # # delta = ['a', 'b']
    # delta = ['a', 'b', 'c']
    #
    # # Start State
    # q0 = 'q0'
    #
    # # Final States
    # # F = ['q2']
    # F = ['q3']
    #
    # # Transitions
    # sigma = {
    #     ('q0', 'a'): ['q1'],
    #     ('q0', 'b'): ['q2'],
    #     ('q1', 'b'): ['q2'],
    #     ('q1', 'a'): ['q3'],
    #     ('q2', 'c'): ['q0', 'q3'],
    # }
    # print("\nGiven Finite Automaton:", end="")
    # finite_automaton_lab_2 = FiniteAutomaton.FiniteAutomaton(Q, delta, sigma, q0, F)
    # finite_automaton_lab_2.print_variables()
    # finite_automaton_lab_2.draw_graph("FA_lab_2")
    #
    # print("\nConverted Given Finite Automaton to Regular Grammar:", end="")
    # grammar_from_finite_automaton_lab_2 = finite_automaton_lab_2.to_grammar(choice=0)
    # grammar_from_finite_automaton_lab_2.print_variables()
    #
    # is_NFA, ambiguous_states = finite_automaton_lab_2.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # print("Attempt to Convert NFA to DFA...")
    # choice = 1
    # if input("Want to construct Complete DFA? (Y/N): ").lower() == "n":
    #     choice = 0
    # DFA = finite_automaton_lab_2.to_DFA(choice)
    # DFA.print_variables()
    # DFA.draw_graph("NFA_to_DFA_lab_2")
    #
    # # Example of NFA
    # nfa_example = FiniteAutomaton.FiniteAutomaton(Q=['S', 'A', 'B', 'C'],
    #                                               delta=['a', 'b', 'c'],
    #                                               q0='S',
    #                                               sigma={
    #                                                     ('S', 'a'): ['A'],
    #                                                     ('S', 'b'): ['B'],
    #                                                     ('A', 'a'): ['C'],
    #                                                     ('A', 'b'): ['B'],
    #                                                     ('B', 'c'): ['S', 'C']
    #                                               },
    #                                               F=['C'])
    # nfa_example.print_variables()
    #
    # is_NFA, ambiguous_states = nfa_example.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # print("Attempt to Convert NFA to DFA...")
    # choice = 1
    # if input("Want to construct Complete DFA? (Y/N): ").lower() == "n":
    #     choice = 0
    # DFA = nfa_example.to_DFA(choice)
    # DFA.print_variables()
    # DFA.draw_graph("NFA_to_DFA_example_1")
    #
    # nfa_example_2 = FiniteAutomaton.FiniteAutomaton(Q=['q0', 'q1', 'q2', 'q3'],
    #                                                 delta=['a', 'b', 'c'],
    #                                                 q0='q0',
    #                                                 sigma={
    #                                                     ('q0', 'a'): ['q1', 'q0'],
    #                                                     ('q1', 'b'): ['q2'],
    #                                                     ('q1', 'c'): ['q1'],
    #                                                     ('q2', 'b'): ['q3'],
    #                                                     ('q3', 'a'): ['q1']
    #                                                 },
    #                                                 F=['q2'])
    # nfa_example_2.print_variables()
    #
    # is_NFA, ambiguous_states = nfa_example_2.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")
    #
    # print("Attempt to Convert NFA to DFA...")
    # choice = 1
    # if input("Want to construct Complete DFA? (Y/N): ").lower() == "n":
    #     choice = 0
    # DFA = nfa_example_2.to_DFA(choice)
    # DFA.print_variables()
    # DFA.draw_graph("NFA_to_DFA_example_2")
    #
    # Example of Grammars
    # extended_left_regular_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                                 V_t={'a', 'b', 'c'},
    #                                                 P={
    #                                                     'S': {"Aab"},
    #                                                     'A': {"Aab", "B"},
    #                                                     'B': {"a"}
    #                                                 },
    #                                                 S="S")
    # extended_left_regular_grammar.print_variables()
    # extended_left_regular_grammar.check_type_grammar()

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

    # extended_right_regular_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                                  V_t={'a', 'b', 'c'},
    #                                                  P={
    #                                                      'S': {"aaA", 'abB', 'aaB'},
    #                                                      'A': {"baA", "B"},
    #                                                      'B': {"a"}
    #                                                  },
    #                                                  S="S")
    # extended_right_regular_grammar.print_variables()
    # extended_right_regular_grammar.check_type_grammar()

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

    # left_regular_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                        V_t={'a', 'b', 'c'},
    #                                        P={
    #                                            'S': {"Bb", 'Ac'},
    #                                            'A': {"Sa", "Ac"},
    #                                            'B': {"a"}
    #                                        },
    #                                        S="S")
    # left_regular_grammar.print_variables()
    # left_regular_grammar.check_type_grammar()

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

    # right_regular_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                         V_t={'a', 'b', 'c'},
    #                                         P={
    #                                             'S': {"aA", 'bB'},
    #                                             'A': {"bA", "B"},
    #                                             'B': {"a"}
    #                                         },
    #                                         S="S")
    # right_regular_grammar.print_variables()
    # right_regular_grammar.check_type_grammar()

    # NFA = right_regular_grammar.to_finite_automaton()
    # is_NFA, ambiguous_states = NFA.NFA_or_DFA()
    # if is_NFA:
    #     print("Finite Automaton is: Non-Deterministic")
    #     print("Ambiguous States:")
    #     for (state, term), next_states in ambiguous_states.items():
    #         print("\u03C3" + str((state, term)), "-", next_states)
    # else:
    #     print("Finite Automaton is: Deterministic")

    # DFA = NFA.to_DFA(choice=1)

    # context_free_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                        V_t={'a', 'b', 'c'},
    #                                        P={
    #                                            'S': {"aA", 'bB'},
    #                                            'A': {"BbA", "BA"},
    #                                            'B': {"a"}
    #                                        },
    #                                        S="S")
    # context_free_grammar.print_variables()
    # context_free_grammar.check_type_grammar()
    #
    # context_sensitive_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                             V_t={'a', 'b', 'c'},
    #                                             P={
    #                                                 'S': {"aA", 'bB'},
    #                                                 'AS': {"BbA", "BA"},
    #                                                 'B': {"a"}
    #                                             },
    #                                             S="S")
    # context_sensitive_grammar.print_variables()
    # context_sensitive_grammar.check_type_grammar()
    #
    # unrestricted_grammar = Grammar.Grammar(V_n={'S', 'A', 'B'},
    #                                        V_t={'a', 'b', 'c'},
    #                                        P={
    #                                            'S': {"aA", 'bB'},
    #                                            'AS': {"BbA", "B"},
    #                                            'B': {"a"}
    #                                        },
    #                                        S="S")
    # unrestricted_grammar.print_variables()
    # unrestricted_grammar.check_type_grammar()
