from typing import List

from v_token import *


def include(text, items):
    for item in items:
        if item in text:
            return True
    return False


def includeNumber(text):
    return include(text, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])


def removeQuotation(token):
    return token.replace("\"", "").replace("\'", "")


def type_convert(token):
    if token == "":
        return token
    if token[0] == "#":
        # print(f"$comment : {token}")
        return ""

    if token[0] == "\"" and token[-1] == "\"" or token[0] == "\'" and token[-1] == "\'":
        return token

    if token[0] == "[" and token[-1] == "]":
        return token

    if includeNumber(token) and include(token, ".") and not include(token, ["\"", "\'"]):
        return float(token)
    elif includeNumber(token) and include(token, ".") and include(token, ["\"", "\'"]):
        return removeQuotation(token)

    elif includeNumber(token) and not include(token, ".") and not include(token, ["\"", "\'"]):
        return int(token)
    elif includeNumber(token) and not include(token, ".") and include(token, ["\"", "\'"]):
        return removeQuotation(token)
    else:
        return token


def lex(text):
    pos = 0
    letters = list(text)
    token = ""
    tokens = []

    while not pos >= len(letters):
        c = str(letters[pos])
        if c.isspace():
            tok = type_convert(token)
            if tok != "":
                tokens.append(tok)
            token = ""
        else:
            token += c
        pos += 1

    if token != "":
        tokens.append(type_convert(token))

    return tokens


def is_symbol(c: str) -> bool:
    # exclude "_"
    return c in "!@#$%^&*()-+={},.:;"


def is_digit(c: str) -> bool:
    return c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def is_whitespace(c: str) -> bool:
    return c in [" ", "\t"]


def is_newline(c: str) -> bool:
    return c in ["\n", "\r"]


def keyword_exchange(keyword: str) -> TokenType:
    if keyword == "true":
        return TokenType.TRUE
    if keyword == "false":
        return TokenType.FALSE
    if keyword == "null":
        return TokenType.NULL
    return TokenType.IDENT


class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.letters = list(text)

    def is_eof(self) -> bool:
        return self.pos >= len(self.letters)

    def prev(self) -> str:
        return self.letters[self.pos - 1]

    def curt(self) -> str:
        return self.letters[self.pos]

    def next(self) -> str:
        return self.letters[self.pos + 1]

    def go_next(self):
        self.pos += 1

    def go_prev(self):
        self.pos -= 1

    def consume_newline(self):
        nls = ""
        s_pos = self.pos
        while not self.is_eof():
            char = self.curt()
            if is_newline(char):
                nls += char
            else:
                break
            self.go_next()
        e_pos = self.pos
        return Token(TokenType.NEWLINE, nls, s_pos, e_pos)

    def consume_whitespace(self):
        whites = ""
        s_pos = self.pos
        while not self.is_eof():
            char = self.curt()
            if is_whitespace(char):
                whites += char
            else:
                break
            self.go_next()
        e_pos = self.pos
        return Token(TokenType.WHITESPACE, whites, s_pos, e_pos)

    def consume_keyword(self):
        key = ""
        s_pos = self.pos
        while not self.is_eof():
            char = self.curt()
            if is_newline(char) or is_whitespace(char) or is_symbol(char):
                break
            else:
                key += char
            self.go_next()
        e_pos = self.pos
        return Token(keyword_exchange(key), key, s_pos, e_pos)

    def consume_numeric(self):
        num = ""
        s_pos = self.pos
        while not self.is_eof():
            char = self.curt()
            if char.isdigit() or char == ".":
                num += char
            else:
                break
            self.go_next()
        e_pos = self.pos

        # check dot's location
        if "." in num:
            if num[0] == "." or num[-1] == ".":
                raise Exception("Dot must not be at the beginning or end.")
            if len(num) - len(num.replace(".", "")) > 1:
                raise Exception("There must not be more than one dot.")
            typ = TokenType.FLOAT
        else:
            typ = TokenType.INT

        return Token(typ, num, s_pos, e_pos)

    def consume_string(self):
        string = ""
        quotation_count = 0

        s_pos = self.pos

        while not self.is_eof():
            char = self.curt()
            if char == "\"":
                string += "\""
                if self.pos != 0 and self.prev() == "\\":
                    string += self.curt()
                    self.go_next()
                else:
                    quotation_count += 1
                    self.go_next()
                    if quotation_count >= 2:
                        break
            else:
                string += char
                self.go_next()

        e_pos = self.pos

        return Token(TokenType.STRING, string, s_pos, e_pos)

    def consume_comment(self):
        s_pos = self.pos
        comment = ""
        while not self.is_eof():
            tk = self.curt()
            if is_newline(tk):
                break
            else:
                comment += tk
            self.go_next()
        e_pos = self.pos
        return Token(TokenType.COMMENT, comment, s_pos, e_pos)

    def consume_symbol(self):
        s_pos = self.pos
        char = self.curt()
        if char == "#":
            return self.consume_comment()
        else:
            self.go_next()
            e_pos = self.pos
            return Token(TokenType.SYMBOL, char, s_pos, e_pos)

    def consume_illegal(self):
        s_pos = self.pos
        char = self.curt()
        self.go_next()
        e_pos = self.pos
        return Token(TokenType.ILLEGAL, char, s_pos, e_pos)

    def consume_eof(self):
        s_pos = self.pos
        e_pos = self.pos + 1
        return Token(TokenType.EOF, "", s_pos, e_pos)

    def consume_addr(self):
        s_pos = self.pos
        addr = ""
        while not self.is_eof():
            tk = self.curt()
            if tk == "]":
                addr += tk
                self.go_next()
                break
            else:
                addr += tk
            self.go_next()
        e_pos = self.pos
        return Token(TokenType.ADDRESS, addr, s_pos, e_pos)

    def lex(self) -> List[Token]:
        tokens = []
        while not self.is_eof():
            char = self.curt()
            if char == "\"":
                tokens.append(self.consume_string())
            elif is_digit(char):
                tokens.append(self.consume_numeric())
            elif char == "[":
                tokens.append(self.consume_addr())
            elif is_symbol(char):
                sym = self.consume_symbol()
                if sym.typ != TokenType.COMMENT:
                    tokens.append(sym)
            elif is_whitespace(char):
                _ = self.consume_whitespace()
            elif is_newline(char):
                tokens.append(self.consume_newline())
            elif char.isalpha() or char == "_":
                tokens.append(self.consume_keyword())
            else:
                tokens.append(self.consume_illegal())
        tokens.append(self.consume_eof())
        return tokens
