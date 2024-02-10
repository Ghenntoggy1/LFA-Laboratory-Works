class FiniteAutomaton:
    # Some state variables as needed.
    #    {Q, Sigma, delta, q0, F}
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def string_belong_to_language(self, input_string):
        # Current state is q0 - Start State
        current_state = [self.q0]
        # next_state = []
        # Iterate over the Input String taking char by char
        for char in input_string:
            # Check if current state is Null, which became during the process next state. If yes, return false -
            # no possible next state for a specific terminal term and current state
            if current_state is None:
                return False

            # next_state = []
            # there might be multiple possible next states from a current state, so we iterate over them
            for state in current_state:
                # Try to get from the dictionary next state by the state
                try:
                    current_state = self.delta[(state, char)]
                    # next_state.append(current_state)
                except KeyError:
                    return False
        else:
            # When entire string is parsed, check whether the final state is an accepted state
            # for possible_state in next_state:
            if "" in current_state:
                return True
            else:
                return False

    def print_variables(self):
        print("Q:", self.Q)
        print("Sigma:", self.sigma)
        print("Delta:", self.delta)
        print("q0:", self.q0)
        print("F:", self.F)

