import unittest
from lexer import *


def is_same_token(expect: Token, actual: Token) -> bool:
    if expect.typ != actual.typ:
        return False
    if expect.data != actual.data:
        return False

    if expect.s_pos != actual.s_pos:
        return False

    if expect.e_pos != actual.e_pos:
        return False

    return True


class TokenTest(unittest.TestCase):
    def test_consume_string(self):
        # (name, want, test-value)
        tests = [
            ("2quo.str", Token(TokenType.STRING, "hello", 0, 7), "\"hello\""),
            ("2quo.int", Token(TokenType.STRING, "123", 0, 5), "\"123\""),
            ("2quo.float", Token(TokenType.STRING, "123.6\'", 0, 8), "\"123.6\'\""),
        ]
        print(">> test_consume_string <<\n")
        for t in tests:
            print(f"<-- {t[0]}")
            lexer = Lexer(t[2])
            want = t[1].string()
            actual = lexer.consume_string().string()
            print("want:", want)
            print("actual:", actual)
            self.assertEqual(want, actual)
            print("--->\n")

    def test_consume_numeric(self):
        tests = [
            ("int", Token(TokenType.INT, "123", 0, 3), "123"),
            ("float", Token(TokenType.FLOAT, "123.6", 0, 5), "123.6"),
            ("float.err", None, "123..6")
        ]
        print(">> test_consume_numeric <<\n")
        for t in tests:
            print(f"<-- {t[0]}")
            lexer = Lexer(t[2])
            want = t[1]
            try:
                actual = lexer.consume_numeric().string()
            except Exception as e:
                if want is None:
                    print(f"[EXPECTED-ERR]: {str(e)}")
                    print("--->\n")
                    continue
                else:
                    print(e)
                    break
            want = want.string()
            print("want:", want)
            print("actual:", actual)
            self.assertEqual(want, actual)
            print("--->\n")

    def test_consume_newline(self):
        tests = [
            ("2newline", Token(TokenType.NEWLINE, "\n\n", 0, 2), "\n\n"),
        ]
        print(">> test_consume_newline <<\n")
        for t in tests:
            print(f"<-- {t[0]}")
            lexer = Lexer(t[2])
            want = t[1]
            try:
                actual = lexer.consume_newline().string()
            except Exception as e:
                if want is None:
                    print(f"[EXPECTED-ERR]: {str(e)}")
                    print("--->\n")
                    continue
                else:
                    print(e)
                    break
            want = want.string()
            print("want:", want)
            print("actual:", actual)
            self.assertEqual(want, actual)
            print("--->\n")

    def test_consume_whitespace(self):
        tests = [
            ("2whitespace", Token(TokenType.WHITESPACE, "\t ", 0, 2), "\t "),
        ]
        print(">> test_consume_whitespace <<\n")
        for t in tests:
            print(f"<-- {t[0]}")
            lexer = Lexer(t[2])
            want = t[1]
            try:
                actual = lexer.consume_whitespace().string()
            except Exception as e:
                if want is None:
                    print(f"[EXPECTED-ERR]: {str(e)}")
                    print("--->\n")
                    continue
                else:
                    print(e)
                    break
            want = want.string()
            print("want:", want)
            print("actual:", actual)
            self.assertEqual(want, actual)
            print("--->\n")

    def test_consume_keyword(self):
        tests = [
            ("true", Token(TokenType.TRUE, "true", 0, 4), "true"),
            ("false", Token(TokenType.FALSE, "false", 0, 5), "false"),
            ("null", Token(TokenType.NULL, "null", 0, 4), "null"),

            ("var", Token(TokenType.IDENT, "var", 0, 3), "var"),
            ("true1", Token(TokenType.IDENT, "true1", 0, 5), "true1"),
        ]
        print(">> test_consume_keyword <<\n")
        for t in tests:
            print(f"<-- {t[0]}")
            lexer = Lexer(t[2])
            want = t[1]
            try:
                actual = lexer.consume_keyword().string()
            except Exception as e:
                if want is None:
                    print(f"[EXPECTED-ERR]: {str(e)}")
                    print("--->\n")
                    continue
                else:
                    print(e)
                    break
            want = want.string()
            print("want:", want)
            print("actual:", actual)
            self.assertEqual(want, actual)
            print("--->\n")

    def test_lex(self):
        tests = [
            ("set_reg_a 1",
             [
                 Token(TokenType.IDENT, "set_reg_a", 0, 9),
                 Token(TokenType.WHITESPACE, " ", 9, 10),
                 Token(TokenType.INT, "1", 10, 11)
             ],
             "set_reg_a 1"),
        ]
        print(">> test_lex <<\n")
        for t in tests:
            print(f"<-- {t[0]}")
            lexer = Lexer(t[2])
            expect = t[1]
            actual = lexer.lex()
            if len(expect) != len(actual):
                raise Exception("no match. expect: " + str(len(expect)) + ", actual: " + str(len(actual)))
            for i in range(len(expect)):
                m = is_same_token(expect[i], actual[i])
                if not m:
                    raise Exception(f"expect: {expect[i].string()}\nactual: {actual[i].string()}")



if __name__ == '__main__':
    unittest.main()
