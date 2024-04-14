import unittest
from .. import Grammar

class UnitTestsEpsilonElimination(unittest.TestCase):
    def setUp(self):
        V_n = {"S", "X", "Y"}
        V_t = {"0", "1"}
        P = {
            "S": {"XYX"},
            "X": {"0X", "epsilon"},
            "Y": {"1Y", "epsilon"},
        }
        S = "S"
        type_grammar = 2
        self.grammar1 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B", "C", "D"}
        V_t = {"a", "b"}
        P = {
            "S": {"AC", "bA", "B", "aA"},
            "A": {"epsilon", "aS", "ABAb"},
            "B": {"a", "AbSA"},
            "C": {"abC"},
            "D": {"AB"}
        }
        S = "S"
        type_grammar = 2
        self.grammar2 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B"}
        V_t = {"a", "b"}
        P = {
            "S": {"epsilon"},
            "A": {"B"},
            "B": {"a"},
        }
        S = "S"
        type_grammar = 2
        self.grammar3 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B", "D"}
        V_t = {"a", "b", "d"}
        P = {
            "S": {"dB", "AB"},
            "A": {"d", "dS", "aAaAb", "epsilon"},
            "B": {"a", "aS", "A"},
            "D": {"Aba"}
        }
        S = "S"
        type_grammar = 2
        self.grammar4 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B", "C", "D"}
        V_t = {"a", "b", "c"}
        P = {
            "S": {"ABC", "aA", "bB", "CD", "epsilon"},
            "A": {"aA", "Aa", "D", "B"},
            "B": {"bB", "BC", "C", "epsilon"},
            "C": {"cC", "Cc", "D"},
            "D": {"AD", "aD", "B"},
            "E": {"epsilon", "S"}
        }
        S = "S"
        type_grammar = 2
        self.grammar5 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)

    def test_eliminate_epsilon_productions_1(self):
        new_P = self.grammar1.eliminate_epsilon_productions()
        new_P = self.grammar1.eliminate_unit_productions(new_P=new_P)
        expected_new_P = {
            "S": {"XYX", "XY", "YX", "Y", "XX", "X"},
            "X": {"0X", "0"},
            "Y": {"1Y", "1"}
        }
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_epsilon_productions_2(self):
        new_P = self.grammar2.eliminate_epsilon_productions()
        new_P = self.grammar2.eliminate_unit_productions(new_P=new_P)
        expected_new_P = {
            "S": {"AC", "bA", "B", "aA", "C", "b", "a"},
            "A": {"aS", "ABAb", "ABb", "BAb", "Bb"},
            "B": {"a", "AbSA", "AbS", "bS", "bSA"},
            "C": {"abC"},
            "D": {"AB", "B"}
        }
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_epsilon_productions_3(self):
        new_P = self.grammar3.eliminate_epsilon_productions()
        new_P = self.grammar4.eliminate_unit_productions(new_P=new_P)
        expected_new_P = {
            "A": {"B"},
            "B": {"a"}
        }
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_epsilon_productions_4(self):
        new_P = self.grammar4.eliminate_epsilon_productions()
        new_P = self.grammar4.eliminate_unit_productions(new_P=new_P)
        expected_new_P = {
            "S": {"dB", "AB", "d", "aS", "aAaAb", "aab", "aAab", "aaAb", "a", "dS"},
            "A": {"d", "dS", "aAaAb", "aAab", "aaAb", "aab"},
            "B": {"dS", "d", "aAaAb", "aaAb", "aAab", "aab", "aS", "a"},
            "D": {"Aba", "ba"}
        }
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_epsilon_productions_5(self):
        new_P = self.grammar5.eliminate_epsilon_productions()
        new_P = self.grammar5.eliminate_unit_productions(new_P=new_P)
        expected_new_P = {
            "S": {"ABC", "aA", "bB", "C", "CD", "A", "AB", "AC", "B", "BC", "a", "b", "D"},
            "A": {"aA", "Aa", "D", "B", "a"},
            "B": {"bB", "BC", "C", "b", "B"},
            "C": {"cC", "Cc", "D", "c"},
            "D": {"AD", "aD", "B", "A", "D", "a"},
            "E": {"S"}
        }
        self.assertEqual(new_P, expected_new_P)

if __name__ == "__main__":
    unittest.main()
