# Random is used to choose randomly a derivation from the Dictionary with all the rules and constrains.
import random
import re
from re import sub
from itertools import chain, combinations



def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class Grammar:
    # Constructor with some state variables as needed.
    # {V_n, V_t, P, S}
    def __init__(self, V_n=None, V_t=None, P=None, S=None, type=None):
        self.type_grammar = type
        if V_n is None or V_t is None or P is None or S is None:
            self.create_grammar()
        else:
            self.V_n = V_n
            self.V_t = V_t
            self.P = P
            for v in self.P.values():
                for deriv in v:
                    if deriv == "epsilon":
                        v.remove(deriv)
                        v.add("\u03B5")
            self.S = S
            if type is None:
                self.check_type_grammar()

    # Print function to easy print the variables in the console.
    def print_variables(self):
        print("\nV_n =", self.V_n)
        print("V_t =", self.V_t)
        print("S =", self.S)
        print("P = {")
        for (k, v) in self.P.items():
            print("  " + k, "->", v)
        print("}")

    def create_grammar(self):
        print("CREATE YOUR OWN GRAMMAR:")

        V_n = input("INPUT NON-TERMINAL TERMS SEPARATED BY COMMA: ")
        V_n = V_n.split(",")
        print(V_n)
        self.V_n = V_n

        V_t = input("INPUT TERMINAL TERMS SEPARATED BY COMMA: ")
        V_t = V_t.split(",")
        print(V_t)
        self.V_t = V_t

        S = input("INPUT START TERM: ")
        print(S)
        self.S = S

        print(
            "INPUT RULES (SEPARATED BY COMMA \"{LEFT-HAND SIDE},{RIGHT-HAND SIDE}\"): ")
        P = {}
        while True:
            rule_string = input("")
            rule = rule_string.split(",")
            print(rule)
            LHS = rule[0]
            print(LHS)
            if rule[1] == "epsilon":
                rule[1] = "\u03B5"
            if LHS in P:
                P[LHS].append(rule[1])
            else:
                P[LHS] = [rule[1]]
            print(f"{rule[0]} -> {rule[1]}")
            if input("CONTINUE? (Y/N) ").lower() == "n":
                break
        self.P = P

        self.check_type_grammar()

    def convert_to_Chomsky_Normal_Form(self):
        if self.type_grammar == 2:
            print("\nPerforming Conversion to Chomsky Normal Form...")
            print("\nPerforming Elimination of \u03B5-productions...")
            new_P = self.eliminate_epsilon_productions()

            print("\nPerforming Elimination of unit-productions...")
            new_P = self.eliminate_unit_productions(new_P)

            print("Performing Elimination of unproductive Symbols...")
            new_P, new_V_n = self.eliminate_unproductive_symbols(new_P)

            print("\nPerforming Elimination of inaccessible symbols...")
            new_P, new_V_n = self.eliminate_inaccessible_symbols(new_P, new_V_n)

            # TODO: Conversion to CNF
            print("\nConverting to Chomsky Normal Form...")
            new_V_t = self.V_t.copy()
            if "\u03B5" in new_V_t:
                new_V_t.remove("\u03B5")
            new_S = self.S

            CNF_P = {}

            old_P = new_P.copy()
            for (LHS, RHS) in new_P.items():
                new_RHS = set()
                for production in RHS:
                    new_RHS.add(tuple(production))
                new_P[LHS] = new_RHS

            has_new_rules = True
            iteration = 0
            while has_new_rules:
                copy_P = new_P.copy()
                iteration += 1
                print("Iteration {}".format(iteration))
                for (LHS, RHS) in new_P.items():
                    for production in set(RHS):
                        if type(production) is tuple:
                            production_list = list(production)
                        else:
                            break
                        if len(production_list) == 1 and production_list[0] in new_V_t:
                            print(f"DELETED RULE: {LHS} -> {production}")
                            copy_P[LHS].remove(production)
                            copy_P[LHS].add("".join(production_list))
                            print(f"ADDED RULE: {LHS} -> {"".join(production_list)}")
                            print("P = {")
                            for (k, v) in copy_P.items():
                                print("  " + k, "->", v)
                            print("}")
                        else:
                            if len(production_list) >= 2:
                                copy_old_list = production
                                copy_P[LHS].remove(production)
                                for symbol in production_list:
                                    if symbol in new_V_t:
                                        new_Non_Terminal = symbol.upper() + "(" + symbol + ")"
                                        new_V_n.add(new_Non_Terminal)
                                        production_list[production_list.index(symbol)] = new_Non_Terminal
                                        if new_Non_Terminal not in copy_P:
                                            copy_P[new_Non_Terminal] = {symbol}
                                            print(f"ADDED RULE: {new_Non_Terminal} -> {symbol}")
                                            print("P = {")
                                            for (k, v) in copy_P.items():
                                                print("  " + k, "->", v)
                                            print("}")
                                        else:
                                            copy_P[new_Non_Terminal].add(symbol)
                                if len(production_list) == 2:
                                    copy_P[LHS].add("".join(production_list))
                                    print(f"DELETED RULE: {LHS} -> {copy_old_list}")
                                    print(f"ADDED RULE: {LHS} -> {"".join(production_list)}")
                                    print("P = {")
                                    for (k, v) in copy_P.items():
                                        print("  " + k, "->", v)
                                    print("}")
                                else:
                                    new_production = [production_list[0]]
                                    rest_production = production_list[1:len(production_list)]

                                    non_terminal_to_post = ""
                                    lst_existing_new_non_terminal = set([key for key in copy_P.keys() if re.match(r'^D\(\d+\)$', key)])
                                    for key in lst_existing_new_non_terminal:
                                        if ("".join(rest_production) == "".join("".join(item) for item in copy_P[key])
                                                and re.match(r'^D\(\d+\)$', key)):
                                            non_terminal_to_post = key
                                    if non_terminal_to_post == "":
                                        new_int = len(lst_existing_new_non_terminal) + 1
                                        non_terminal_to_post = f"D({str(new_int)})"
                                    new_production.append(non_terminal_to_post)
                                    copy_P[non_terminal_to_post] = {tuple(rest_production)}

                                    print(f"DELETED RULE: {LHS} -> {"".join(production_list)}")
                                    print(f"ADDED RULE: {LHS} -> {"".join(new_production)}")
                                    print(f"NEW ADDED RULE: {non_terminal_to_post} -> {"".join(rest_production)}")
                                    copy_P[LHS].add("".join(new_production))
                                    print("P = {")
                                    for (k, v) in copy_P.items():
                                        print("  " + k, "->", v)
                                    print("}")
                if copy_P == new_P:
                    print("No new Rules.")
                    print("V_n =", set(new_P.keys()))
                    has_new_rules = False
                    print("P = {")
                    for (k, v) in new_P.items():
                        print("  " + k, "->", v)
                    print("}")
                else:
                    new_P = copy_P

            print("CFG IN CHOSMKY NORMAL FORM:")
            print("S =", new_S)
            print("V_t =", new_V_t)
            new_V_n = set(new_P.keys())
            print("V_n =", new_V_n)
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")

            return Grammar(V_n=new_V_n, V_t=new_V_t, P=new_P, S=new_S, type=self.type_grammar)
        else:
            print("Grammar is not of type 2! Can't convert to Chomsky Normal Form!")
            return None

    def eliminate_epsilon_productions(self):
        new_P = {}
        # Declare empty set that will hold symbols from LHS that derive into ε
        set_nullable_symbols = set()
        # Iterate over all the production Rules
        for (LHS, RHS) in self.P.items():
            # Iterate over all the RHS possible derivations
            for production in RHS:
                # If derivation is ε, then add this symbol to the set from above
                if production == "\u03B5":
                    set_nullable_symbols.add(LHS)
                else:
                    if LHS not in new_P:
                        new_P[LHS] = {production}
                    else:
                        new_P[LHS].add(production)

        print("Set of Nullable Symbols =", set_nullable_symbols)

        copy_p = new_P.copy()
        if len(set_nullable_symbols) > 0:
            for nullable_symbol in set_nullable_symbols:
                print("\nFor Nullable Symbol =", nullable_symbol)
                for (LHS, RHS) in new_P.items():
                    new_productions = set()  # Store new productions here
                    for production in RHS:
                        symbols = list(production)
                        indices = [i for i, v in enumerate(symbols) if v == nullable_symbol]
                        power_set = powerset(indices)
                        for replacements in power_set:
                            new_words = list(symbols)
                            for index in replacements:
                                new_words[index] = ""
                            new_production = "".join(new_words)
                            if new_production != production:
                                new_productions.add(new_production)
                            if "" in new_productions:
                                new_productions.remove("")
                    # Update original set after the loop
                    old_productions = copy_p[LHS].copy()
                    copy_p[LHS].update(new_productions)
                    if old_productions != copy_p[LHS]:
                        print(f"OLD RULE: {LHS} -> {old_productions}")
                        print(f"NEW RULE: {LHS} -> {copy_p[LHS]}")
                        print(f"DIFFERENCE: {copy_p[LHS].difference(old_productions)}")

        new_P = copy_p
        if len(set_nullable_symbols) > 0:
            print("\nNew Production Rules without \u03B5-productions:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")
        else:
            print("No \u03B5-productions were found!")
        return new_P

    def eliminate_unit_productions(self, new_P):
        prev_P = new_P.copy()
        copy_p = new_P.copy()
        has_unit_productions = True
        iteration = 0
        while has_unit_productions:
            iteration += 1
            print(f"Iteration {iteration}:")

            has_unit_productions = False
            nr_unit_production = 0

            for (LHS, RHS) in new_P.items():

                RHS_copy = RHS.copy()  # Create a copy of the RHS set
                for production in RHS_copy:
                    if len(production) == 1 and production.isupper():
                        nr_unit_production += 1
                        print(f"Unit Production {nr_unit_production}: {LHS} -> {production}")
                        new_derivations = copy_p[LHS].union(new_P[production])
                        new_derivations.remove(production)
                        copy_p[LHS] = new_derivations
                new_P = copy_p
            for (LHS, RHS) in new_P.items():
                for production in RHS:
                    if len(production) == 1 and production.isupper():
                        has_unit_productions = True

            print(f"New Production Rules after iteration {iteration}:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")
        new_P = copy_p

        # Calculate the difference between new_P and productive_productions
        difference = {}
        for symbol in new_P:
            if symbol in prev_P:
                difference_set = prev_P[symbol] - new_P[symbol]
                if len(difference_set) != 0:
                    difference[symbol] = difference_set

        if len(difference.keys()) != 0:
            print("\nNew Production Rules without \u03B5-productions and unit-productions:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")
            print("Difference between previous Production Rules and Production Rules without Unit Productions:")
            print("Expanded/Removed Unit Productions = {")
            for (k, v) in difference.items():
                print("  " + k, "->", v)
            print("}")
        else:
            print("No unit production expanded/removed.")
            print("\nProduction Rules stay the same:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")
        return new_P

    def eliminate_unproductive_symbols(self, new_P):
        productive_symbols_set = set()
        productive_productions = {}

        iteration = 0
        has_unproductive_symbols = True

        print("Finding Productive Symbols:")
        while has_unproductive_symbols:
            iteration += 1
            print(f"Iteration {iteration}:")

            prev_productive_productions = productive_productions.copy()
            for (LHS, RHS) in new_P.items():
                for production in RHS:
                    if len(production) == 1:
                        if production.islower() and production in self.V_t:
                            if LHS not in productive_symbols_set:
                                print(f"{LHS} -> {production}")
                            productive_symbols_set.add(LHS)
                            if LHS not in productive_productions:
                                productive_productions[LHS] = {production}
                            else:
                                productive_productions[LHS].add(production)
                    else:
                        is_productive = True
                        for symbol in production:
                            if symbol.isupper():
                                # if is_productive:
                                if symbol not in productive_symbols_set:
                                    is_productive = False
                        if is_productive:
                            print(f"{LHS} -> {production}")
                            productive_symbols_set.add(LHS)
                            if LHS not in productive_productions:
                                productive_productions[LHS] = {production}
                            else:
                                productive_productions[LHS].add(production)

            print(f"New Production Rules after iteration {iteration}:")
            print("P = {")
            for (k, v) in productive_productions.items():
                print("  " + k, "->", v)
            print("}")

            # Check if there's any change in productive_productions
            if prev_productive_productions == productive_productions:
                print("No more productive productions")
                has_unproductive_symbols = False

        # Calculate the difference between new_P and productive_productions
        difference = {}
        for symbol in productive_productions:
            if symbol in new_P:
                difference_set = new_P[symbol] - productive_productions[symbol]
                if len(difference_set) != 0:
                    difference[symbol] = difference_set

        if len(difference.keys()) != 0:
            print("\nSet of Productive Non-Terminal Terms:", productive_symbols_set)
            print("\nNew Production Rules without \u03B5-productions, unit-productions, unproductive-productions:")
            print("P = {")
            for (k, v) in productive_productions.items():
                print("  " + k, "->", v)
            print("}")

            print("Difference between previous Production Rules and productive Production Rules:")
            print("Removed Unproductive Rules = {")
            for (k, v) in difference.items():
                print("  " + k, "->", v)
            print("}")
        else:
            print("No unproductive rules removed.")
            print("\nProduction Rules stay the same:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")
        return productive_productions, productive_symbols_set


    def eliminate_inaccessible_symbols(self, new_P, new_V_n):
        prev_P = new_P.copy()
        copy_P = new_P.copy()
        accessible_symbols_set = set()
        for (LHS, RHS) in new_P.items():
            for production in RHS:
                if LHS == self.S and len(production) == 1 and production in self.V_t:
                    accessible_symbols_set.add(LHS)
                for symbol in production:
                    if symbol.isupper() and symbol != LHS:
                        accessible_symbols_set.add(symbol)

        inaccessible_symbols_set = new_V_n.difference(accessible_symbols_set)
        print("Set of Accessible Symbols =", accessible_symbols_set)
        print("Set of Inaccessible Symbols =", inaccessible_symbols_set)
        for inaccessible_symbol in inaccessible_symbols_set:
            try:
                copy_P.pop(inaccessible_symbol)
            except KeyError:
                continue

        new_V_n = accessible_symbols_set
        new_P = copy_P

        # Calculate the difference between new_P and productive_productions
        removed_symbols_with_productions = {}
        for symbol in prev_P:
            if symbol not in new_P:
                removed_symbols_with_productions[symbol] = prev_P[symbol]

        removed_symbols = set()
        for symbol in prev_P:
            if symbol not in new_P:
                removed_symbols.add(symbol)

        if len(removed_symbols) != 0:
            print("\nNew Set of Non-Terminal Terms:", new_V_n)
            print("\nNew Production Rules without \u03B5-productions, unit-productions, unproductive-productions "
                  "and inaccessible symbols:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")
            print("Non-terminal symbols removed:", removed_symbols)
            print("Difference between previous Production Rules and Production Rules without inaccessible symbols:")
            print("Rules that were removed:")
            print("Removed_Rules = {")
            for symbol, productions in removed_symbols_with_productions.items():
                print(f"  {symbol} -> {productions}")
            print("}")
        else:
            print("No non-terminal symbols removed.")
            print("\nProduction Rules stay the same:")
            print("P = {")
            for (k, v) in new_P.items():
                print("  " + k, "->", v)
            print("}")

        return new_P, new_V_n


    def check_type_grammar(self):
        # Check if Grammar is Extended Regular Grammar
        is_extended = False

        # Check if Grammar is Left Linear Regular Grammar
        is_left_linear = True

        # Check if Grammar is Right Linear Regular Grammar
        is_right_linear = True

        # Check if Grammar is Regular Grammar
        is_type_3 = True

        # Check if Grammar is Context-Free Grammar
        is_type_2 = True

        # Check if Grammar is Context-Sensitive Grammar
        is_type_1 = True

        # Check if Grammar is Unrestricted Grammar
        is_type_0 = True

        # Check if Grammar is Invalid
        is_invalid = False

        for LHS, RHS_list in self.P.items():
            # If Grammar is Invalid, exit loop.
            if is_invalid:
                break

            # Edge-Case: Not valid Non-Terminal Term Left-Hand Side
            for term in LHS:
                if term not in self.V_n and term.isupper():
                    is_invalid = True
                    break

            # Check if already invalid => no need to check further
            if is_invalid:
                break
            # Edge-Case: Not valid Terminal Term or Non-Terminal Term in Right-Hand Side
            else:
                for production in RHS_list:
                    if production == "\u03B5":
                        self.V_t.add(production)
                    if is_invalid:
                        break
                    for term_prod in production:
                        # Not Valid Terminal Term
                        if term_prod.islower() and term_prod not in self.V_t:
                            print(f"Term {term_prod} is not valid Terminal Term!")
                            is_invalid = True
                            break

                        # Not Valid Non-Terminal Term
                        if term_prod.isupper() and term_prod not in self.V_n:
                            print(f"Term {term_prod} is not valid Non-Terminal Term!")
                            is_invalid = True
                            break

            # If Left-Hand Side has more than one Non-Terminal Term, then Grammar is not Regular and not Context-Free
            if len(LHS) != 1:
                is_type_3 = False
                is_type_2 = False

                # If the length of Left-Hand Side is greater than at least one Right-Hand Side => Grammar is not
                # Context-Sensitive
                for RHS in RHS_list:
                    if len(LHS) > len(RHS):
                        is_type_1 = False

            # If Regular Grammar and first term is Non-Terminal and rest are terminals, then Left Linear Regular Grammar
            if is_type_3:
                for RHS in RHS_list:
                    if len(RHS) == 1 and not RHS[0].islower():
                        # If Right-Hand Side has one Non-Terminal Term that => Grammar is not Regular
                        # if RHS[0] not in self.V_n:
                        is_type_3 = False
                        break
                        # else:
                        #     continue

                    # If Regular Grammar and first term is Non-Terminal and rest are terminals,
                    # then Left Linear Regular Grammar
                    if RHS[0].isupper():
                        if not is_left_linear:
                            is_type_3 = False
                            break
                        is_right_linear = False
                        for rest_terms in RHS[1:]:
                            for rest_term in rest_terms:
                                if rest_term.isupper():
                                    is_type_3 = False
                                    break
                    # If Regular Grammar and last term is Non-Terminal and rest has at least one Non-Terminal,
                    # then Grammar is not Regular
                    if RHS[-1].isupper():
                        if not is_right_linear:
                            is_type_3 = False
                            break
                        is_left_linear = False
                        for rest_terms in RHS[:-1]:
                            for rest_term in rest_terms:
                                if rest_term.isupper():
                                    is_type_3 = False
                                    break

                    # Check if Right-Hand Side is longer than 2 terms => Extended Regular Grammar
                    if len(RHS) > 2 and is_type_3:
                        is_extended = True

        print("Grammar is: ", end="")
        if is_invalid:
            self.type_grammar = -1
            print("Invalid")
        elif is_type_3:
            self.type_grammar = 3
            if is_left_linear:
                if is_extended:
                    print("Type 3 - Extended Left Linear Regular Grammar")
                else:
                    print("Type 3 - Left Linear Regular Grammar")
            elif is_right_linear:
                if is_extended:
                    print("Type 3 - Extended Right Linear Regular Grammar")
                else:
                    print("Type 3 - Right Linear Regular Grammar")
        elif is_type_2:
            self.type_grammar = 2
            print("Type 2 - Context-Free Grammar")
        elif is_type_1:
            self.type_grammar = 1
            print("Type 1 - Context-Sensitive Grammar")
        elif is_type_0:
            self.type_grammar = 0
            print("Type 0 - Unrestricted Grammar")

    # # Method for generation of Strings based on the Rules.

    # def generate_string(self, max_length):
    #     # Edge-case: If Start term is not present in the Non-Terminal List, then return empty string = cannot be
    #     # generated string from this variables
    #     if self.S not in self.V_n:
    #         print(f"Start Symbol: {self.S} is not present in Non-Terminal Terms")
    #         return None
    #
    #     # String used in order to append more easily and manipulate String variables
    #     generated_string = []
    #     print(f"{self.S} -> ", end="")
    #     # First call of the generation of the string that will go recursively
    #     self.__generate_next_string(generated_string, self.S, max_length)
    #     # Return the generated String that is formed in the end of the recursion call.
    #     return generated_string
    #
    # def __generate_next_string(self, current_word, term, max_length):
    #     # Edge-case: word is too long (avoid infinite recursion)
    #     if len(current_word) >= max_length:
    #         current_word.append(term[-1])  # add last non-terminal term in order to display correctly the generated word
    #         return  # exit recursion
    #
    #     # Case: if there is a rule/produce for this specific Non-Terminal Term -> goes into recursion for the next term
    #     if term in self.P:
    #         # Get all possible derivations for current non-terminal term
    #         curr_derivation_list = self.P[term]
    #
    #         # Get one random derivation from the Produce List
    #         curr_derivation = random.choice(curr_derivation_list)
    #
    #         # Check if last term is Non-Terminal, then add -> at the end, else - do not add
    #         if curr_derivation[-1].isupper():
    #             print(f'{"".join(current_word)}{curr_derivation} -> ', end="")
    #         elif len(curr_derivation) > 1 and 'q' in curr_derivation[curr_derivation.index("q"):] and curr_derivation[
    #             curr_derivation.index("q") + 1].isnumeric():
    #             print(f'{"".join(current_word)}{curr_derivation} -> ', end="")
    #         else:
    #             print(f'{"".join(current_word)}{curr_derivation}', end="")
    #
    #         # For every term, iterate again recursively: ensures adding the terminal term and going for
    #         # the non-terminal one in another recursion
    #         if curr_derivation[-1].isupper():
    #             for separate_term in curr_derivation:
    #                 self.__generate_next_string(current_word, separate_term, max_length)
    #         elif len(curr_derivation) == 1:
    #             self.__generate_next_string(current_word, curr_derivation[0], max_length)
    #         elif 'q' in curr_derivation[curr_derivation.index("q"):] and curr_derivation[
    #             curr_derivation.index("q") + 1].isnumeric():
    #             for separate_term in curr_derivation:
    #                 if separate_term != "q" and not separate_term.isnumeric():
    #                     self.__generate_next_string(current_word, separate_term, max_length)
    #                 elif separate_term == "q" and curr_derivation[curr_derivation.index("q") + 1].isnumeric():
    #                     self.__generate_next_string(current_word, curr_derivation[
    #                                                               curr_derivation.index("q"):curr_derivation.index(
    #                                                                   "q") + 2], max_length)
    #
    #     # Case: if there is no rule/produce for this specific Non-Terminal Term -> ends recursion
    #     else:
    #         # Edge-case: if the Term is Non-Terminal and has no further derivation
    #         if term not in self.P and (term.isupper()):
    #             current_word.append(term)
    #             print(f"\nNon-Terminal Term: {term} is not present in Rules Dictionary!", end="")
    #         # Case: if the Term is a Terminal Term
    #         else:
    #             current_word.append(term)  # add the terminal term and exits recursion

    # # Method to convert to Finite Automaton

    # def to_finite_automaton(self):
    #     # States - will hold the possible states = Non-Terminal Terms
    #     Q = self.V_n
    #     new_element_terminal_state = "q_f"
    #     Q.append(new_element_terminal_state)
    #     # Alphabet = Terminal Terms
    #     delta = self.V_t
    #     # Start state = Start term
    #     q0 = self.S
    #     # Final states
    #     F = [new_element_terminal_state]
    #     # Transitions Set
    #     sigma = {}
    #     # Iterate over all the Rules in the Product Dictionary (current state = non-terminal term from the dictionary)
    #     for current_state, derivations_list in self.P.items():
    #         # Iterate over all the derivations for a Non-Terminal Term
    #         for derivation in derivations_list:
    #             # Get the list of characters/terms in the string/derivation
    #             terms = list(derivation)
    #             # Current input term is the part of the derivation that is of Terminal terms
    #             current_input_term = ""
    #             # Next State is the Non-Terminal term in the derivation string
    #             next_state = "q_f"
    #
    #             try:
    #                 state_index = terms.index("q")
    #             except ValueError:
    #                 state_index = -1
    #             if state_index >= 0 and terms[state_index + 1].isnumeric():
    #                 terminal_terms = terms[:state_index]
    #                 for term in terminal_terms:
    #                     current_input_term += term
    #                 next_state = "".join(terms[state_index: state_index + 2])
    #             else:
    #                 for term in terms:
    #                     if term.islower() and term in delta:
    #                         current_input_term += term
    #                     if term.isupper() and term in Q:
    #                         next_state = term
    #
    #             # Initialize a list for the Left Hand side of the transition function (current state, current input
    #             # term)
    #             LHS = tuple([current_state, current_input_term])
    #
    #             # Place it in the dictonary as a tuple as key and its value is assigned to the next state.
    #             if LHS in sigma.keys():
    #                 sigma[LHS].append(next_state)
    #             else:
    #                 sigma[LHS] = [next_state]
    #
    #     # Return object of type FiniteAutomaton, with the parameters that I found above
    #     return FiniteAutomaton.FiniteAutomaton(Q, delta, sigma, q0, F)


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