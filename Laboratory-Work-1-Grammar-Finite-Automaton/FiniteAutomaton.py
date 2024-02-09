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
        # Current state is q0
        current_state = [self.q0]
        # Iterate over the Input String taking char by char
        for char in input_string:
            # Transition to the next state using the current state and input alphabet
            if current_state is None:
                return False

            for state in current_state:
                try:
                    current_state = self.delta[(state, char)]
                except KeyError:

                    return False

        else:
            # When entire string is parsed, check whether the final state is an accepted state

            if "" in current_state:

                return True
            else:

                return False

        # while True:
        #     current_word = input_string[:current_length]
        #     print("Current Word: ", current_word)
        #     if self.delta.contains([current_state, current_word[-1]]):
        #         current_state = self.delta.get([current_state, current_word[-1]])
        #     # for LHS, RHS in self.delta.items():
        #     #     if LHS[0] == current_state and LHS[1] == current_word[-1]:
        #     #         print(LHS, RHS)
        #     #         current_state = RHS
        #
        #     current_length += 1
        #     if current_length > len(input_string):
        #         break
        #
        # if current_state == "":
        #     print("Accepted")
        # else:
        #     print("Rejected")


    def print_variables(self):
        print("Q:", self.Q)
        print("Sigma:", self.sigma)
        print("Delta:", self.delta)
        print("q0:", self.q0)
        print("F:", self.F)

