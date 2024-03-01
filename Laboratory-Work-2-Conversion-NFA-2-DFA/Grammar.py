# Random is used to choose randomly a derivation from the Dictionary with all the rules and constrains.
import random
import FiniteAutomaton


class Grammar:
    # Constructor with some state variables as needed.
    # {V_n, V_t, P, S}
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = S

    def generate_string(self, max_length):
        # Edge-case: If Start term is not present in the Non-Terminal List, then return empty string = cannot be
        # generated string from this variables
        if self.S not in self.V_n:
            print(f"Start Symbol: {self.S} is not present in Non-Terminal Terms")
            return None

        # String used in order to append more easily and manipulate String variables
        generated_string = []
        print(f"{self.S} -> ", end="")
        # First call of the generation of the string that will go recursively
        self.__generate_next_string(generated_string, self.S, max_length)
        # Return the generated String that is formed in the end of the recursion call.
        return generated_string

    def __generate_next_string(self, current_word, term, max_length):
        # Edge-case: word is too long (avoid infinite recursion)
        if len(current_word) >= max_length:
            current_word.append(term[-1])  # add last non-terminal term in order to display correctly the generated word
            return  # exit recursion

        # Case: if there is a rule/produce for this specific Non-Terminal Term -> goes into recursion for the next term
        if term in self.P:
            # Get all possible derivations for current non-terminal term
            curr_derivation_list = self.P[term]

            # Get one random derivation from the Produce List
            curr_derivation = random.choice(curr_derivation_list)

            # Check if last term is Non-Terminal, then add -> at the end, else - do not add
            if curr_derivation[-1].isupper() or ('q' in curr_derivation[-2:] and curr_derivation[-1].isnumeric()):
                print(f'{"".join(current_word)}{curr_derivation} -> ', end="")
            else:
                print(f'{"".join(current_word)}{curr_derivation}', end="")

            # For every term, iterate again recursively: ensures adding the terminal term and going for
            # the non-terminal one in another recursion
            if curr_derivation[-1].isupper():
                for separate_term in curr_derivation:
                    self.__generate_next_string(current_word, separate_term, max_length)
            elif curr_derivation[-2:].contains('q') and curr_derivation[-1].isnumeric():
                self.__generate_next_string(current_word, curr_derivation, max_length)
        # Case: if there is no rule/produce for this specific Non-Terminal Term -> ends recursion
        else:
            # Edge-case: if the Term is Non-Terminal and has no further derivation
            if term not in self.P and (term.isupper()):
                current_word.append(term)
                print(f"\nNon-Terminal Term: {term} is not present in Rules Dictionary!", end="")
            # Case: if the Term is a Terminal Term
            else:
                current_word.append(term)  # add the terminal term and exits recursion

    def to_finite_automaton(self):
        # Terminal States - will hold the possible states = Non-Terminal Terms + another terminal state
        Q = self.V_n
        new_element_terminal_state = "q_f"
        Q.append(new_element_terminal_state)
        # Alphabet = Terminal Terms
        delta = self.V_t
        # Start state = Start term
        q0 = self.S
        # Final states
        F = [new_element_terminal_state]
        # Transitions Set
        sigma = {}
        # Iterate over all the Rules in the Product Dictionary (current state = non-terminal term from the dictionary)
        for current_state, derivations_list in self.P.items():
            # Iterate over all the derivations for a Non-Terminal Term
            for derivation in derivations_list:
                # Get the list of characters/terms in the string/derivation
                terms = list(derivation)
                # Current input term is the part of the derivation that is of Terminal terms
                current_input_term = ""
                # Next State is the Non-Terminal term in the derivation string
                next_state = "q_f"
                for term in terms:
                    if term.islower() and term in delta:
                        current_input_term += term
                    if term.isupper() and term in Q:
                        next_state = term
                # Initialize a list for the Left Hand side of the transition function (current state, current input
                # term)
                LHS = tuple([current_state, current_input_term])

                # Place it in the dictonary as a tuple as key and its value is assigned to the next state.
                if LHS in sigma.keys():
                    sigma[LHS].append(next_state)
                else:
                    sigma[LHS] = [next_state]

        # Return object of type FiniteAutomaton, with the parameters that I found above
        return FiniteAutomaton.FiniteAutomaton(Q, delta, sigma, q0, F)


# Rudimentary Method for finding final states.  

# # Check if in the derivation list we can achieve a final state - if the rule derives into an expression
# # without non-terminal term.
# # Iterate over the rules
# for non_terminal_term, derivations_list in self.P.items():
#     # Iterate other the derivations of this specific rule
#     for derivation in derivations_list:
#         # boolean that will show if the specific Non-Terminal is a final state
#         flag = True
#         # Iterate term by term over the derivation
#         for term in derivation:
#             # Check if it has Non-Terminal Terms or if the term is not in the alphabet, then flag is set to
#             # false - therefore this Non-Terminal is not a final state
#             if term.isupper() or term not in delta:
#                 flag = False
#         # If flag is still true and term is not contained in the Final states list, then add it to the list
#         if flag and term not in F:
#             F.append(non_terminal_term)
