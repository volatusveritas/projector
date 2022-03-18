import unittest
from projector import *




class EvaluationTests(unittest.TestCase):
    def test_basic_operators(self):
        self.assertEqual(evaluate("5+5"), 10)
        self.assertEqual(evaluate("5-5"), 0)
        self.assertEqual(evaluate("5*5"), 25)
        self.assertEqual(evaluate("5/5"), 1)

    def test_precedence(self):
        self.assertEqual(evaluate("3+4*5"), 23)
        self.assertEqual(evaluate("30-(4+4*2+1)"), 17)
        self.assertEqual(evaluate("-1+4*3/2"), 5)
        self.assertEqual(evaluate("4*3/2-1+0"), 5)

    def test_parentheses(self):
        self.assertEqual(evaluate("(5+5)"), 10)
        self.assertEqual(evaluate("(10 + 10) - (10 + 10)"), 0)
        self.assertEqual(evaluate("5*(2+1)"), 15)
        self.assertEqual(evaluate("5+(2*(4/2))-1"), 8)

    def test_variables(self):
        self.assertEqual(evaluate("x = 5"))




if __name__ == "__main__":
    unittest.main()
