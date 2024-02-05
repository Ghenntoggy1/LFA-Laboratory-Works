# Random is used to choose randomly a derivation from the Dictionary with all the rules and constrains.
import random


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
            if curr_derivation[-1].isupper():
                print(f'{"".join(current_word)}{curr_derivation} -> ', end="")
            else:
                print(f'{"".join(current_word)}{curr_derivation}', end="")

            # For every term, iterate again recursively: ensures adding the terminal term and going for
            # the non-terminal one in another recursion
            for separate_term in curr_derivation:
                self.__generate_next_string(current_word, separate_term, max_length)
        # Case: if there is no rule/produce for this specific Non-Terminal Term -> ends recursion
        else:
            # Edge-case: if the Term is Non-Terminal and has no further derivation
            if term not in self.P and term.isupper():
                current_word.append(term)
                print(f"\nNon-Terminal Term: {term} is not present in Rules Dictionary!", end="")
            # Case: if the Term is a Terminal Term
            else:
                current_word.append(term)  # add the terminal term and exits recursion
