import unittest
from .. import Grammar


class UnitTestsUnproductiveElimination(unittest.TestCase):
    def setUp(self):
        V_n = {"S", "X", "Y", "Z"}
        V_t = {"0", "1"}
        P = {
            "S": {"XYX", "XY", "YX", "1Y", "1", "XX", "0X", "0"},
            "X": {"0X", "0"},
            "Y": {"1Y", "1"}
        }
        S = "S"
        type_grammar = 2
        self.grammar1 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B", "C", "D"}
        V_t = {"a", "b"}
        P = {
            "S": {"AC", "bA", "aA", "b", "a", "AbSA", "abC", "AbS", "bS", "bSA"},
            "A": {"aS", "ABAb", "ABb", "BAb", "Bb"},
            "B": {"a", "AbSA", "AbS", "bS", "bSA"},
            "C": {"abC"},
            "D": {"AB", "AbSA", "AbS", "bSA", "bS", "a"}
        }
        S = "S"
        type_grammar = 2
        self.grammar2 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B"}
        V_t = {"a", "b"}
        P = {
            "A": {"aA"},
            "B": {"a"}
        }
        S = "S"
        type_grammar = 2
        self.grammar3 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B", "D", "E"}
        V_t = {"a", "b", "d"}
        P = {
            "S": {"dB", "AB", "d", "aS", "aAaAb", "aab", "aAab", "aaAb", "a", "dS"},
            "A": {"d", "dS", "aAaAb", "aAab", "aaAb", "aab"},
            "B": {"dS", "d", "aAaAb", "aaAb", "aAab", "aab", "aS", "a"},
            "D": {"Aba", "ba"},
            "E": {"aE", "BE"}
        }
        S = "S"
        type_grammar = 2
        self.grammar4 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)
        V_n = {"S", "A", "B", "C", "D", "E"}
        V_t = {"a", "b", "c"}
        P = {
            "S": {"ABC", "aA", "bB", "CD", "AB", "AC", "BC", "a", "b", "Aa", "cC", "c", "aD", "Cc", "AD"},
            "A": {"Aa", "a", "aA", "cC", "BC", "aD", "Cc", "b", "c", "AD", "bB"},
            "B": {"b", "BC", "bB", "Aa", "cC", "c", "Cc", "aA", "aD", "a", "AD"},
            "C": {"cC", "Cc", "BC", "Aa", "b", "c", "aA", "aD", "a", "AD", "bB"},
            "D": {"AD", "aD", "Aa", "BC", "cC", "a", "aA", "c", "b", "a", "Cc", "bB"},
            "E": {"BC", "Aa", "ABC", "cC", "CD", "b", "a", "AB", "AD", "Cc", "AC", "bB", "aD", "aA", "c"}
        }
        S = "S"
        type_grammar = 2
        self.grammar5 = Grammar.Grammar(V_t=V_t, V_n=V_n, P=P, S=S, type=type_grammar)

    def test_eliminate_unproductive_productions_1(self):
        new_P = self.grammar1.P
        new_P, new_V_n = self.grammar1.eliminate_unproductive_symbols(new_P=new_P)
        print(new_V_n)
        expected_new_P = {
            "S": {"XYX", "XY", "YX", "1Y", "1", "XX", "0X", "0"},
            "X": {"0X", "0"},
            "Y": {"1Y", "1"}
        }
        expected_new_V_n = {"S", "X", "Y"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_unproductive_productions_2(self):
        new_P = self.grammar2.P
        new_P, new_V_n = self.grammar2.eliminate_unproductive_symbols(new_P=new_P)
        print(new_V_n)
        expected_new_P = {
            "S": {"bA", "aA", "b", "a", "AbSA", "AbS", "bS", "bSA"},
            "A": {"aS", "ABAb", "ABb", "BAb", "Bb"},
            "B": {"a", "AbSA", "AbS", "bS", "bSA"},
            "D": {"AB", "AbSA", "AbS", "bSA", "bS", "a"}
        }
        expected_new_V_n = {"S", "A", "B", "D"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_unproductive_productions_3(self):
        new_P = self.grammar3.P
        new_P, new_V_n = self.grammar3.eliminate_unproductive_symbols(new_P=new_P)
        print(new_V_n)
        expected_new_P = {
            "B": {"a"}
        }
        expected_new_V_n = {"B"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_unproductive_productions_4(self):
        new_P = self.grammar4.P
        new_P, new_V_n = self.grammar4.eliminate_unproductive_symbols(new_P=new_P)
        print(new_V_n)
        expected_new_P = {
            "S": {"dB", "AB", "d", "aS", "aAaAb", "aab", "aAab", "aaAb", "a", "dS"},
            "A": {"d", "dS", "aAaAb", "aAab", "aaAb", "aab"},
            "B": {"dS", "d", "aAaAb", "aaAb", "aAab", "aab", "aS", "a"},
            "D": {"Aba", "ba"}
        }
        expected_new_V_n = {"S", "A", "B", "D"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_eliminate_unproductive_productions_5(self):
        new_P = self.grammar5.P
        new_P, new_V_n = self.grammar5.eliminate_unproductive_symbols(new_P=new_P)
        expected_new_P = {
            "S": {"ABC", "aA", "bB", "CD", "AB", "AC", "BC", "a", "b", "Aa", "cC", "c", "aD", "Cc", "AD"},
            "A": {"Aa", "a", "aA", "cC", "BC", "aD", "Cc", "b", "c", "AD", "bB"},
            "B": {"b", "BC", "bB", "Aa", "cC", "c", "Cc", "aA", "aD", "a", "AD"},
            "C": {"cC", "Cc", "BC", "Aa", "b", "c", "aA", "aD", "a", "AD", "bB"},
            "D": {"AD", "aD", "Aa", "BC", "cC", "a", "aA", "c", "b", "a", "Cc", "bB"},
            "E": {"BC", "Aa", "ABC", "cC", "CD", "b", "a", "AB", "AD", "Cc", "AC", "bB", "aD", "aA", "c"}
        }
        expected_new_V_n = {"S", "A", "B", "C", "D", "E"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

if __name__ == "__main__":
    unittest.main()
