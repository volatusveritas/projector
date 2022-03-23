import unittest

from projector import interpret




class EvaluationTests(unittest.TestCase):
    def test_basic_operators(self):
        self.assertEqual(interpret.evaluate("5+5"), 10)
        self.assertEqual(interpret.evaluate("5-5"), 0)
        self.assertEqual(interpret.evaluate("5*5"), 25)
        self.assertEqual(interpret.evaluate("5/5"), 1)

    def test_precedence(self):
        self.assertEqual(interpret.evaluate("3+4*5"), 23)
        self.assertEqual(interpret.evaluate("30-(4+4*2+1)"), 17)
        self.assertEqual(interpret.evaluate("-1+4*3/2"), 5)
        self.assertEqual(interpret.evaluate("4*3/2-1+0"), 5)

    def test_parentheses(self):
        self.assertEqual(interpret.evaluate("(5+5)"), 10)
        self.assertEqual(interpret.evaluate("(10 + 10) - (10 + 10)"), 0)
        self.assertEqual(interpret.evaluate("5*(2+1)"), 15)
        self.assertEqual(interpret.evaluate("5+(2*(4/2))-1"), 8)
