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

    def test_lex_vol(self):
        with open("if_new_format_idea.vol", "r") as f:
            program = f.read()
        lx = Lexer(program)
        tokens = lx.lex()
        for t in tokens:
            print(t.string())
            if t.typ == TokenType.NEWLINE:
                print()


if __name__ == '__main__':
    unittest.main()
