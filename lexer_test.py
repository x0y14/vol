import unittest

from lexer import *


class LexerTest(unittest.TestCase):
    def test_lex(self):
        self.assertEqual([123], lex("123"))
        self.assertEqual([float(123.0)], lex("123.0"))
        self.assertEqual(["123"], lex('"123"'))
        self.assertEqual(["123.1"], lex('"123.1"'))
        self.assertEqual(["text"], lex('text'))

        self.assertEqual(["add", 3], lex('add 3'))
        self.assertEqual(["add", 5.4], lex('add 5.4'))
        self.assertEqual(["add", "5.4"], lex('add \"5.4\"'))

        with open("./program.vol", "r") as f:
            program = f.read()
        self.assertEqual(
            ["set_reg_a", 0,
             "set_reg_b", 1,
             "add_b_to_a",
             "jump", 4,
             "exit"], lex(program))


if __name__ == '__main__':
    unittest.main()
