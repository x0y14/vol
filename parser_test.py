import unittest
from lexer import *
from parser import *
from v_token import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        with open("if_new_format_idea.vol", "r") as f:
            program = f.read()
        lx = Lexer(program)
        tokens = lx.lex()
        for t in tokens:
            print(t.string())
            if t.typ == TokenType.NEWLINE:
                print()
        ps = Parser(tokens)
        ops = ps.parse()
        for op in ops:
            print(op.string())
            # print(op)


if __name__ == '__main__':
    unittest.main()
