import unittest
from .. import Grammar


class UnitTestsPreCNFConversion(unittest.TestCase):
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
            "S": {"epsilon", "a"},
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

    def test_make_pre_CNF_conversion_1(self):
        new_P = self.grammar1.eliminate_epsilon_productions()
        new_P = self.grammar1.eliminate_unit_productions(new_P=new_P)
        new_P, new_V_n = self.grammar1.eliminate_unproductive_symbols(new_P=new_P)
        new_P, new_V_n = self.grammar1.eliminate_inaccessible_symbols(new_P=new_P, new_V_n=new_V_n)
        expected_new_P = {
            "S": {'XX', '0X', '1Y', '1', '0', 'YX', 'XYX', 'XY'},
            "X": {'0X', '0'},
            "Y": {'1Y', '1'}
        }
        expected_new_V_n = {'X', 'S', 'Y'}

        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_make_pre_CNF_conversion_2(self):
        new_P = self.grammar2.eliminate_epsilon_productions()
        new_P = self.grammar2.eliminate_unit_productions(new_P=new_P)
        new_P, new_V_n = self.grammar2.eliminate_unproductive_symbols(new_P=new_P)
        new_P, new_V_n = self.grammar2.eliminate_inaccessible_symbols(new_P=new_P, new_V_n=new_V_n)
        expected_new_P = {
            "S": {"bA", "aA", "b", "a", "AbSA", "AbS", "bS", "bSA"},
            "A": {"aS", "ABAb", "ABb", "BAb", "Bb"},
            "B": {"a", "AbSA", "AbS", "bS", "bSA"}
        }
        expected_new_V_n = {"S", "A", "B"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_make_pre_CNF_conversion_3(self):
        new_P = self.grammar3.eliminate_epsilon_productions()
        new_P = self.grammar3.eliminate_unit_productions(new_P=new_P)
        new_P, new_V_n = self.grammar3.eliminate_unproductive_symbols(new_P=new_P)
        new_P, new_V_n = self.grammar3.eliminate_inaccessible_symbols(new_P=new_P, new_V_n=new_V_n)
        expected_new_P = {
            "S": {"a"}
        }
        expected_new_V_n = {"S"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_make_pre_CNF_conversion_4(self):
        new_P = self.grammar4.eliminate_epsilon_productions()
        new_P = self.grammar4.eliminate_unit_productions(new_P=new_P)
        new_P, new_V_n = self.grammar4.eliminate_unproductive_symbols(new_P=new_P)
        new_P, new_V_n = self.grammar4.eliminate_inaccessible_symbols(new_P=new_P, new_V_n=new_V_n)
        expected_new_P = {
            "S": {"dB", "AB", "d", "aS", "aAaAb", "aab", "aAab", "aaAb", "a", "dS"},
            "A": {"d", "dS", "aAaAb", "aAab", "aaAb", "aab"},
            "B": {"dS", "d", "aAaAb", "aaAb", "aAab", "aab", "aS", "a"}
        }
        expected_new_V_n = {"S", "A", "B"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

    def test_make_pre_CNF_conversion_5(self):
        new_P = self.grammar5.eliminate_epsilon_productions()
        new_P = self.grammar5.eliminate_unit_productions(new_P=new_P)
        new_P, new_V_n = self.grammar5.eliminate_unproductive_symbols(new_P=new_P)
        new_P, new_V_n = self.grammar5.eliminate_inaccessible_symbols(new_P=new_P, new_V_n=new_V_n)
        expected_new_P = {
            "S": {"ABC", "aA", "bB", "CD", "AB", "AC", "BC", "a", "b", "Aa", "cC", "c", "aD", "Cc", "AD"},
            "A": {"Aa", "a", "aA", "cC", "BC", "aD", "Cc", "b", "c", "AD", "bB"},
            "B": {"b", "BC", "bB", "Aa", "cC", "c", "Cc", "aA", "aD", "a", "AD"},
            "C": {"cC", "Cc", "BC", "Aa", "b", "c", "aA", "aD", "a", "AD", "bB"},
            "D": {"AD", "aD", "Aa", "BC", "cC", "a", "aA", "c", "b", "a", "Cc", "bB"}
        }
        expected_new_V_n = {"S", "A", "B", "C", "D"}
        self.assertEqual(new_V_n, expected_new_V_n)
        self.assertEqual(new_P, expected_new_P)

if __name__ == "__main__":
    unittest.main()
