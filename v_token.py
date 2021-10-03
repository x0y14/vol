from enum import IntEnum, auto


class TokenType(IntEnum):
    ILLEGAL = auto()

    STRING = auto()
    INT = auto()
    FLOAT = auto()

    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    IDENT = auto()

    NEWLINE = auto()
    WHITESPACE = auto()

    # !@#$%^&*()_-+={}[]
    SYMBOL = auto()

    EOF = auto()


def TokenType_string(tktyp: TokenType):
    if tktyp == TokenType.ILLEGAL:
        return "ILLEGAL"
    elif tktyp == TokenType.STRING:
        return "STRING"
    elif tktyp == TokenType.INT:
        return "INT"
    elif tktyp == TokenType.FLOAT:
        return "FLOAT"
    elif tktyp == TokenType.TRUE:
        return "TRUE"
    elif tktyp == TokenType.FALSE:
        return "FALSE"
    elif tktyp == TokenType.NULL:
        return "NULL"
    elif tktyp == TokenType.IDENT:
        return "IDENT"
    elif tktyp == TokenType.NEWLINE:
        return "NEWLINE"
    elif tktyp == TokenType.WHITESPACE:
        return "WHITESPACE"
    elif tktyp == TokenType.SYMBOL:
        return "SYMBOL"
    elif tktyp == TokenType.EOF:
        return "EOF"


class Token:
    def __init__(self, typ: TokenType, data: str, s_pos: int, e_pos: int):
        self.typ = typ
        self.data = data
        self.s_pos = s_pos
        self.e_pos = e_pos

    def string(self):
        # return f"typ: {TokenType_string(self.typ)}, data: {self.data}, s_pos: {self.s_pos}, e_pos: {self.e_pos}"
        return "typ: {typ:10} | data: {data!r:15} | s_pos: {s:3} | e_pos: {e:3}".format(
            typ=TokenType_string(self.typ),
            data=self.data,
            s=self.s_pos,
            e=self.e_pos)
