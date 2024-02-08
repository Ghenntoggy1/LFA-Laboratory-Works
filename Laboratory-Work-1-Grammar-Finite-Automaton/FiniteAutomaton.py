class FiniteAutomaton:
    # Some state variables as needed.
    #    {Q, Sigma, delta, q0, F}
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    # def string_belong_to_language(self, inputString):

    def print_variables(self):
        print("Q:", self.Q)
        print("Sigma:", self.sigma)
        print("Delta:", self.delta)
        print("q0:", self.q0)
        print("F:", self.F)

