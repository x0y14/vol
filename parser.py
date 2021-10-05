from typing import List
from v_token import Token, TokenType, TokenType_string
from v_operation import *
from v_command import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def curt(self) -> Token:
        return self.tokens[self.pos]

    def next(self) -> Token:
        return self.tokens[self.pos + 1]

    def go_next(self):
        self.pos += 1

    def is_eof(self) -> bool:
        return self.pos >= len(self.tokens)

    # def consume_comment(self):
    #     comment = ""
    #     while not self.is_eof():
    #         tk = self.curt()
    #         if tk.typ == TokenType.NEWLINE or tk.typ == TokenType.EOF:
    #             break
    #         else:
    #             comment += tk.data
    #         self.go_next()
    #     print(f"typ: COMMENT    {comment}")

    def consume_newline(self):
        while not self.is_eof():
            nl = self.curt()
            if nl.typ == TokenType.NEWLINE:
                self.go_next()
            else:
                break

    def consume_labeled_ident(self):
        label = self.curt().data
        # consume label
        self.go_next()

        colon = self.curt()
        if colon.data != ":":
            raise Exception(f"SyntaxError: expect `:`, but found {colon.data}({colon.typ})")
        # consume :
        self.go_next()

        nl = self.curt()
        if nl.typ != TokenType.NEWLINE:
            raise Exception(f"SyntaxError: expect `NEWLINE`, but found {nl.data}({nl.typ})")
        # consume newline
        self.consume_newline()

        op = self.consume_ident()
        op.label = label
        return op

    def consume_ident(self):
        tk = self.curt()
        command = tk.data
        if command not in Commands:
            raise Exception(f"Unknown Command: `{command}`({tk.typ})")

        args = []
        args_count: int = Commands[command]

        # consume command
        self.go_next()

        for i in range(args_count):
            arg = self.curt()
            # print(f"arg: {arg.string()}")
            if arg.typ == TokenType.INT:
                args.append(int(arg.data))
            elif arg.typ == TokenType.FLOAT:
                args.append(float(arg.data))
            elif arg.typ == TokenType.STRING:
                args.append(str(arg.data))
            elif arg.typ == TokenType.TRUE:
                args.append(True)
            elif arg.typ == TokenType.FALSE:
                args.append(False)
            elif arg.typ == TokenType.NULL:
                args.append(None)
            elif arg.typ == TokenType.IDENT:
                args.append(str(arg.data))
            else:
                args.append(arg)
            self.go_next()

        nl = self.curt()
        if nl.typ == TokenType.NEWLINE:
            self.consume_newline()

        return Operation(command=command, args=args, label="")

    def parse(self):
        ops: List[Operation] = []
        while not self.is_eof():

            tk = self.curt()
            if tk.typ == TokenType.IDENT:
                nx = self.next()
                if nx.typ == TokenType.SYMBOL and nx.data == ":":
                    # labeled
                    ops.append(self.consume_labeled_ident())
                else:
                    ops.append(self.consume_ident())
            else:
                self.go_next()

            # print(tk.string())
            # if tk.typ == TokenType.NEWLINE:
            #     print()

        return ops

