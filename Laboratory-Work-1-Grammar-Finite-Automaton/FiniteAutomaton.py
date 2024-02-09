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
        next_state = ""
        # String that will be constructed iteratively and tracked by state
        current_length = 1

        # Get first initial next State from Start state
        # for LHS, RHS in self.delta.items():
        #     if LHS[0] == string[-1] and LHS[1] == current_state:
        #         next_state = RHS

        # flag = True
        # while flag:
        #     string = inputString[:current_length]
        #     for LHS, RHS in self.delta.items():
        #         if LHS[1] == string[-1] and LHS[0] == current_state:
        #             print(LHS, "-", RHS)
        #             print("String: ", string)
        #             print("Current State: ", current_state)
        #             print("Next State: ", RHS)
        #             current_state = RHS
        #             current_length += 1
        #             break
        #         else:
        #             print(LHS, "-", RHS)
        #             print("String: ", string)
        #             print("Current State: ", current_state)
        #             print("Next State: ", RHS)
        #             flag = False
        # if flag:
        #     print("ACCEPTED")
        # else:
        #     print("REJECTED")
        # print(self.delta)
        for char in input_string:
            # Transition to the next state using the current state and input alphabet
            if current_state is not None:
                for state in current_state:

                    try:
                        current_state = self.delta[(state, char)]
                        # print(char, current_state)
                    except KeyError:
                        print("Rejected")
                        current_state = None
                        break
        else:
            # When entire string is parsed, check whether the final state is an accepted state
            if current_state is not None:
                if "" in current_state:
                    print("Accepted")
                else:
                    print("Rejected")

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

