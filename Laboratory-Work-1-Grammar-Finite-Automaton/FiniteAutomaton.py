class FiniteAutomaton:
    # Some state variables as needed.
    #    {Q, Sigma, delta, q0, F}
    def __init__(self, Q, delta, sigma, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def string_belong_to_language(self, input_string):
        # Edge-case: if Input String contain Terms that are not accepted by the Finite Automaton.
        for term in input_string:
            if term not in self.delta:
                return False

        # Current state is q0 - Start State
        current_state = [self.q0]
        # Iterate over the Input String taking char by char
        for char in input_string:
            # Check if current state is Null, which became during the process next state. If yes, return false -
            # no possible next state for a specific terminal term and current state
            if current_state is None:
                return False
            # This method puts final state on the index 0 of the list.
            current_state.sort()
            # There might be multiple possible next states from a current state, so we iterate over them
            for state in current_state:
                # Try to get from the dictionary next state by the state
                try:
                    # Case: if state is not "", that is final state, then try to get the next state
                    # from the transitions list, which might give Key Error (such transition does not exit in the list
                    # therefore no possible transition for the current state and terminal term => reject the word)
                    if state != '':
                        current_state = self.sigma[(state, char)]
                    # Edge-case: if state is final state, and it is the only possible next State, then return false,
                    # because this term program checks is not the last character in the input string therefore no
                    # possible further transition.
                    elif len(current_state) == 1 and current_state[0] == "":
                        return False
                except KeyError:
                    # As I mentioned, if the transition is not present in the list, it gives error when trying to get
                    # that specific transition, therefore return False aka reject the worc
                    return False
        else:
            # When entire string is parsed, check whether the final state is an accepted state
            # for possible_state in next_state:
            if "" in current_state:
                return True
            else:
                return False

    # Print function to easy print the variables in the console.
    def print_variables(self):
        print("\nQ:", self.Q)
        print("Delta:", self.delta)
        print("Sigma:")
        for (k, v) in self.sigma.items():
            print("\u03C3" + str(k), "-", v)
        print("q0:", self.q0)
        print("F:", self.F)
