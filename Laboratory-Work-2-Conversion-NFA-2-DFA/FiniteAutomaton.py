from graphviz import Digraph
import os
import Grammar


class FiniteAutomaton:
    # Some state variables as needed.
    #    {Q, Sigma, delta, q0, F}
    def __init__(self, Q=None, delta=None, sigma=None, q0=None, F=None):
        if Q is None or delta is None or sigma is None or q0 is None or F is None:
            self.create_finite_automaton()
        else:
            self.Q = Q
            self.sigma = sigma
            self.delta = delta
            self.q0 = q0
            self.F = F

    def create_finite_automaton(self):
        print("CREATE YOUR OWN FINITE AUTOMATON:")

        Q = input("INPUT STATES SEPARATED BY COMMA: ")
        Q = Q.split(",")
        print(Q)
        self.Q = Q

        delta = input("INPUT TERMINAL TERMS SEPARATED BY COMMA: ")
        delta = delta.split(",")
        print(delta)
        self.delta = delta

        q0 = input("INPUT START STATE: ")
        print(q0)
        self.q0 = q0

        F = input("INPUT FINAL STATE: ")
        print(F)
        self.F = [F]

        for final_state in self.F:
            if final_state not in self.Q:
                self.Q.append(final_state)

        print(
            "INPUT TRANSITIONS (SEPARATED BY COMMA \"{STATE},{TERMINAL_TERM},{NEXT_STATE}\") AND USE FOR FINAL STATE \"q_f\": ")
        sigma = {}
        while True:
            transition_string = input("")
            transition = transition_string.split(",")
            print(transition)
            LHS = (transition[0], transition[1])
            print(LHS)
            if LHS in sigma:
                sigma[LHS].append(transition[2])
            else:
                sigma[LHS] = [transition[2]]
            print(f"\u03C3({transition[0]}, {transition[1]}) -> {[transition[2]]}")
            if input("CONTINUE? (Y/N) ").lower() == "n":
                break
        self.sigma = sigma

    def string_belong_to_language(self, input_string):
        print("\nInput String:", input_string)
        # Edge-case: if Input String contain Terms that are not accepted by the Finite Automaton.
        for term in input_string:
            if term not in self.delta:
                return False

        # Current state is q0 - Start State
        current_state = [self.q0]
        # Print Start transition for input string
        print(f"-> {current_state[0] if len(current_state) == 1 else current_state}", end="")
        # Iterate over Input String term by term
        for term in input_string:

            # Print current term
            print(" --" + term, end="--> ")

            # Initialize a set that will contain next possible States to translate into
            next_state = set()
            # Iterate over the current states and try to find next possible State to translate into
            for state in current_state:
                try:
                    # Retrieve all next possible States to translate from current state with current term and iterate
                    # over that list of possible next States and add them to the set that will replace the current state
                    # list
                    for next_state_single in self.sigma[(state, term)]:
                        next_state.add(next_state_single)

                    # Print next states
                    if list(current_state)[-1] == state:
                        print(next_state, end="")

                except KeyError:
                    # KeyError means that no possible transition from current state with terminal term
                    # Check if there are no more possible next states so that don't lose another possible branch
                    if len(current_state) == 1:
                        # Goes into a dead State => Rejected Word
                        print("{q_d}", end="")
                        return False
                    # Else, go to the next possible State and check that one.
                    if list(current_state)[-1] == state:
                        print(next_state, end="")
                    continue
            current_state = next_state
        # Transform list to set so that apply method intersection
        current_state = set(current_state)

        # Check if last possible state list contains final state (Intersection of 2 sets => finds same elements)
        return current_state.intersection(self.F)

    # Print function to easy print the variables in the console.
    def print_variables(self):
        print("\nQ:", self.Q)
        print("Delta:", self.delta)
        print("Sigma:")
        for (k, v) in self.sigma.items():
            print("\u03C3" + str(k), "-", v)
        print("q0:", self.q0)
        print("F:", self.F)

    def draw_graph(self, name):
        graph = Digraph(comment='Graphical Representation of Finite Automaton')
        # Add states to the graph of Finite Automaton
        for state in self.Q:
            if state in self.F:
                graph.attr('node', shape='doublecircle')
            else:
                graph.attr('node', shape='circle')
            if type(state) is list:
                if len(state) == 1:
                    graph.node(state[0])
                else:
                    graph.node("".join(state))
            else:
                graph.node(state)

        # Add transitions to the graph of Finite Automaton
        for (state, term), next_states in self.sigma.items():
            for next_state in next_states:
                if type(state) is tuple:
                    if len(state) == 1:
                        graph.edge(state[0], next_state, label=term)
                    else:
                        graph.edge("".join(state), next_state, label=term)
                else:
                    graph.edge(state, next_state, label=term)

        # Show the State that is Start State
        # Delete from the Graph the outline of the Invisible State
        graph.attr('node', shape='none')
        # Delete the name of the Invisible State
        graph.node('start', label='')
        # Add the edge between Invisible state and Start State
        graph.edge('start', self.q0)

        # Draw the Graph of FA
        path = os.path.dirname(os.path.realpath(__file__)) + "\Graph_Representation\\"
        print(path)
        graph.render(path + name, view=True)

    def to_grammar(self):
        # Non-Terminal Terms - will hold possible Non-Terminal Terms = States
        V_n = self.Q
        # Terminal Terms - will hold possible Terminal Terms = Alphabet
        V_t = self.delta
        # Start Term = Start State
        S = self.q0
        # Product Set - will hold the Rules for the Grammar = Converted from Transition Set
        P = {}
        # Iterate over all the Transitions in the Transitions Dictionary (non-terminal term = current state
        # from the dictionary)
        for (state, term), next_states in self.sigma.items():
            for next_state in next_states:
                if state not in P:
                    P[state] = [term + next_state]
                else:
                    P[state].append(term + next_state)

        for final_state in self.F:
            if final_state not in P:
                P[final_state] = ["\u03B5"]

        return Grammar.Grammar(V_n, V_t, P, S)

    def NFA_or_DFA(self):
        # Initialize boolean for NFA check
        is_NFA = False
        # Initialize a list that will hold the relations with ambiguity
        ambiguous_states = {}
        # Iterate over next_States from state with the same term
        for (state, term), next_states in self.sigma.items():
            # If there are multiple possible unique next_States => ambiguity and choice in options => NFA
            if len(set(next_states)) > 1:
                is_NFA = True
                ambiguous_states[(state, term)] = next_states
                # # No need to iterate further, we know that FA is NFA
                # break
        return is_NFA, ambiguous_states

    def to_DFA(self, choice):
        # Edge-Case: If FA is DFA, no need to convert
        if not self.NFA_or_DFA()[0]:
            print("Finite Automaton is already Deterministic!")
            return self

        # Start State
        q0_DFA = self.q0

        # Alphabet is the same
        delta_DFA = self.delta

        # New State List
        Q_DFA = [[q0_DFA]]

        # New Transition List
        sigma_DFA = {}

        for converted_state in Q_DFA:
            lst = []
            for transition, next_state in self.sigma.items():
                for curr_state in converted_state:
                    if next_state not in lst and curr_state in transition[0]:
                        lst.append(next_state)

            for terminal_term in delta_DFA:
                if len(converted_state) == 1:
                    try:
                        l = [converted_state[0], terminal_term]
                        next_state = self.sigma[tuple(l)]

                        if len(next_state) == 1:
                            sigma_DFA[tuple(l)] = next_state
                        else:
                            sigma_DFA[tuple(l)] = ["".join(next_state)]

                    except KeyError:
                        if choice == 1:
                            l = [converted_state[0], terminal_term]
                            next_state = "q_d"
                            sigma_DFA[tuple(l)] = [next_state]
                else:
                    combined_state = []
                    print(converted_state)

            for state in lst:
                if state not in Q_DFA:
                    Q_DFA.append(state)

        F_DFA = []
        for final_state in self.F:
            for states in Q_DFA:
                if final_state in states:
                    F_DFA.append(states)

        return FiniteAutomaton(Q_DFA, delta_DFA, sigma_DFA, q0_DFA, F_DFA)

# from graphviz import Digraph
# import os
# import Grammar
#
#
# class FiniteAutomaton:
#     # Some state variables as needed.
#     #    {Q, Sigma, delta, q0, F}
#     def __init__(self, Q=None, delta=None, sigma=None, q0=None, F=None):
#         if Q is None or delta is None or sigma is None or q0 is None or F is None:
#             self.create_finite_automaton()
#         else:
#             self.Q = Q
#             self.sigma = sigma
#             self.delta = delta
#             self.q0 = q0
#             self.F = F
#
#     def create_finite_automaton(self):
#         print("CREATE YOUR OWN FINITE AUTOMATON:")
#
#         Q = input("INPUT STATES SEPARATED BY COMMA: ")
#         Q = Q.split(",")
#         print(Q)
#         self.Q = Q
#
#         delta = input("INPUT TERMINAL TERMS SEPARATED BY COMMA: ")
#         delta = delta.split(",")
#         print(delta)
#         self.delta = delta
#
#         q0 = input("INPUT START STATE: ")
#         print(q0)
#         self.q0 = q0
#
#         F = input("INPUT FINAL STATE: ")
#         print(F)
#         self.F = [F]
#
#         for final_state in self.F:
#             if final_state not in self.Q:
#                 self.Q.append(final_state)
#
#         print(
#             "INPUT TRANSITIONS (SEPARATED BY COMMA \"{STATE},{TERMINAL_TERM},{NEXT_STATE}\") AND USE FOR FINAL STATE \"q_f\": ")
#         sigma = {}
#         while True:
#             transition_string = input("")
#             transition = transition_string.split(",")
#             print(transition)
#             LHS = (transition[0], transition[1])
#             print(LHS)
#             if LHS in sigma:
#                 sigma[LHS].append(transition[2])
#             else:
#                 sigma[LHS] = [transition[2]]
#             print(f"\u03C3({transition[0]}, {transition[1]}) -> {[transition[2]]}")
#             if input("CONTINUE? (Y/N) ").lower() == "n":
#                 break
#         self.sigma = sigma
#
#     def string_belong_to_language(self, input_string):
#         print("\nInput String:", input_string)
#         # Edge-case: if Input String contain Terms that are not accepted by the Finite Automaton.
#         for term in input_string:
#             if term not in self.delta:
#                 return False
#
#         # Current state is q0 - Start State
#         current_state = [self.q0]
#         # Print Start transition for input string
#         print(f"-> {current_state[0] if len(current_state) == 1 else current_state}", end="")
#         # Iterate over Input String term by term
#         for term in input_string:
#
#             # Print current term
#             print(" --" + term, end="--> ")
#
#             # Initialize a set that will contain next possible States to translate into
#             next_state = set()
#             # Iterate over the current states and try to find next possible State to translate into
#             for state in current_state:
#                 try:
#                     # Retrieve all next possible States to translate from current state with current term and iterate
#                     # over that list of possible next States and add them to the set that will replace the current state
#                     # list
#                     for next_state_single in self.sigma[(state, term)]:
#                         next_state.add(next_state_single)
#
#                     # Print next states
#                     if list(current_state)[-1] == state:
#                         print(next_state, end="")
#
#                 except KeyError:
#                     # KeyError means that no possible transition from current state with terminal term
#                     # Check if there are no more possible next states so that don't lose another possible branch
#                     if len(current_state) == 1:
#                         # Goes into a dead State => Rejected Word
#                         print("{q_d}", end="")
#                         return False
#                     # Else, go to the next possible State and check that one.
#                     if list(current_state)[-1] == state:
#                         print(next_state, end="")
#                     continue
#             current_state = next_state
#         # Transform list to set so that apply method intersection
#         current_state = set(current_state)
#
#         # Check if last possible state list contains final state (Intersection of 2 sets => finds same elements)
#         return current_state.intersection(self.F)
#
#     # Print function to easy print the variables in the console.
#     def print_variables(self):
#         print("\nQ:", self.Q)
#         print("Delta:", self.delta)
#         print("Sigma:")
#         for (k, v) in self.sigma.items():
#             print("\u03C3" + str(k), "-", v)
#         print("q0:", self.q0)
#         print("F:", self.F)
#
#     def draw_graph(self, name):
#         graph = Digraph(comment='Graphical Representation of Finite Automaton')
#         # Add states to the graph of Finite Automaton
#         for state in self.Q:
#             if state in self.F:
#                 graph.attr('node', shape='doublecircle')
#             else:
#                 graph.attr('node', shape='circle')
#             if type(state) is list:
#                 if len(state) == 1:
#                     graph.node(state[0])
#                 else:
#                     graph.node("".join(state))
#             else:
#                 graph.node(state)
#
#         # Add transitions to the graph of Finite Automaton
#         for (state, term), next_states in self.sigma.items():
#             for next_state in next_states:
#                 if type(state) is tuple:
#                     if len(state) == 1:
#                         graph.edge(state[0], next_state, label=term)
#                     else:
#                         graph.edge("".join(state), next_state, label=term)
#                 else:
#                     graph.edge(state, next_state, label=term)
#
#         # Show the State that is Start State
#         # Delete from the Graph the outline of the Invisible State
#         graph.attr('node', shape='none')
#         # Delete the name of the Invisible State
#         graph.node('start', label='')
#         # Add the edge between Invisible state and Start State
#         graph.edge('start', self.q0)
#
#         # Draw the Graph of FA
#         path = os.path.dirname(os.path.realpath(__file__)) + "\Graph_Representation\\"
#         print(path)
#         graph.render(path + name, view=True)
#
#     def to_grammar(self):
#         # Non-Terminal Terms - will hold possible Non-Terminal Terms = States
#         V_n = self.Q
#         # Terminal Terms - will hold possible Terminal Terms = Alphabet
#         V_t = self.delta
#         # Start Term = Start State
#         S = self.q0
#         # Product Set - will hold the Rules for the Grammar = Converted from Transition Set
#         P = {}
#         # Iterate over all the Transitions in the Transitions Dictionary (non-terminal term = current state
#         # from the dictionary)
#         for (state, term), next_states in self.sigma.items():
#             for next_state in next_states:
#                 if state not in P:
#                     P[state] = [term + next_state]
#                 else:
#                     P[state].append(term + next_state)
#
#         for final_state in self.F:
#             if final_state not in P:
#                 P[final_state] = ["\u03B5"]
#
#         return Grammar.Grammar(V_n, V_t, P, S)
#
#     def NFA_or_DFA(self):
#         # Initialize boolean for NFA check
#         is_NFA = False
#         # Initialize a list that will hold the relations with ambiguity
#         ambiguous_states = {}
#         # Iterate over next_States from state with the same term
#         for (state, term), next_states in self.sigma.items():
#             # If there are multiple possible unique next_States => ambiguity and choice in options => NFA
#             if len(set(next_states)) > 1:
#                 is_NFA = True
#                 ambiguous_states[(state, term)] = next_states
#                 # # No need to iterate further, we know that FA is NFA
#                 # break
#         return is_NFA, ambiguous_states
#
#     def to_DFA(self):
#         # Edge-Case: If FA is DFA, no need to convert
#         if not self.NFA_or_DFA()[0]:
#             print("Finite Automaton is already Deterministic!")
#             return self
#
#         # Start State
#         q0_DFA = self.q0
#
#         # Alphabet is the same
#         delta_DFA = self.delta
#
#         # New State List
#         Q_DFA = [[q0_DFA]]
#
#         # New Transition List
#         sigma_DFA = {}
#
#         for converted_state in Q_DFA:
#             lst = []
#             combined_state = []
#             for transition in self.sigma.keys():
#                 if len(converted_state) == 1:
#                     if converted_state[0] in transition:
#                         if len(self.sigma[transition]) == 1:
#                             if converted_state[0] not in sigma_DFA:
#                                 sigma_DFA[tuple([converted_state[0], transition[1]])] = self.sigma[transition]
#                                 lst.append(self.sigma[transition])
#                             else:
#                                 sigma_DFA[tuple([converted_state[0], transition[1]])] = sigma_DFA[tuple([converted_state[0], transition[1]])] + self.sigma[transition]
#                         else:
#                             if converted_state[0] not in sigma_DFA:
#                                 if len(self.sigma[transition]) > 1:
#                                     lst.append(self.sigma[transition])
#                                     sigma_DFA[tuple([converted_state[0], transition[1]])] = ["".join(self.sigma[transition])]
#                                 else:
#                                     sigma_DFA[tuple([converted_state[0], transition[1]])] = sigma_DFA[tuple([converted_state[0], transition[1]])] + self.sigma[transition]
#                             else:
#                                 sigma_DFA[tuple([converted_state[0], transition[1]])] += self.sigma[transition]
#                 else:
#
#                     for component_state in converted_state:
#                         if component_state in transition:
#                             if len(self.sigma[transition]) == 1:
#                                 if component_state not in sigma_DFA:
#                                     # sigma_DFA[tuple([tuple(converted_state), transition[1]])] = self.sigma[transition]
#                                     if self.sigma[transition] in converted_state[0]:
#                                         continue
#                                     else:
#                                         converted_state[0].append(self.sigma[transition])
#                                 else:
#                                     sigma_DFA[tuple([tuple(converted_state), transition[1]])] = sigma_DFA[tuple([tuple(
#                                         converted_state), transition[1]])] + self.sigma[transition]
#                             else:
#                                 combined_state_track = "".join(self.sigma[transition])
#                                 if component_state not in sigma_DFA:
#                                     # sigma_DFA[tuple([component_state, transition[1]])] = self.sigma[transition]
#                                     combined_state.append(self.sigma[transition])
#                                     print(sigma_DFA)
#                                 else:
#                                     sigma_DFA[tuple([component_state, transition[1]])] += self.sigma[transition]
#                     sigma_DFA[tuple([tuple(converted_state), transition[1]])] = combined_state
#
#             for state in lst:
#                 if len(state) == 1:
#                     if state not in Q_DFA:
#                         Q_DFA.append(state)
#                 else:
#                     if state not in Q_DFA:
#                         Q_DFA.append(state)
#
#         F_DFA = []
#         for states in delta_DFA:
#             for final_state in self.F:
#                 if final_state in states:
#                     F_DFA.append(states)
#
#         return FiniteAutomaton(Q_DFA, delta_DFA, sigma_DFA, q0_DFA, F_DFA)
