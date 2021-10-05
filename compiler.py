import sys
from pprint import pprint

from v_operation import *
from v_token import *
from lexer import *
from parser import *
from v_share import *


class Compiler:
    def __init__(self, path):
        self.filepath = path

        with open(path, "r") as f:
            program = f.read()

        lxr = Lexer(program)
        psr = Parser(lxr.lex())
        self.ops = psr.parse()
        # self.mem_mapping = self.__mem_mapping()

        self.pc = 0
        self.zf = 0
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0

        self.mid = []
        self.mapping = {}

    def mem_mapping(self):
        items = 0
        mapping = {}
        for m in self.mid:
            if m["label"] != "":
                mapping[m["label"]] = items
            items += len(m["raw"])
        self.mapping = mapping
        print("cpr-mapping:")
        print(self.mapping)
        print()

    # pc
    def set_pc(self, n):
        self.pc = n

    def mov_pc(self, n):
        self.pc += n

    # def codegen(self):
    #     lno = 0
    #     mem = []
    #     for op in self.ops:
    #         # print("({:3})  |  {}".format(lno, op.string()))
    #         print([op.command, *op.args], end="")
    #         if op.command in ["jump", "jump_eq", "call", "ret"]:
    #             pass
    #         print()
    #         lno += 1
    #         mem = [*mem, *[op.command, *op.args]]
    #     # print(mem)

    def convert(self):
        lines = []
        for op in self.ops:
            lines.append({"label": op.label, "raw": [op.command, *op.args]})

        self.mid = lines
        print("cpr-mid:")
        pprint(self.mid)
        print()

    def codegen(self) -> str:
        code = ""
        no = 0
        line = ""
        for mid_ in self.mid:
            for item in mid_["raw"]:
                # print("({:3}) ".format(no), end="")
                if item in self.mapping:
                    line += "{} ".format(self.mapping[item])
                else:
                    line += "{} ".format(item)
                no += 1

            code += line + "\n"
            line = ""

        return code


if __name__ == "__main__":
    filepath = sys.argv[1]
    asmpath = sys.argv[2]
    cpr = Compiler(filepath)
    cpr.convert()
    cpr.mem_mapping()
    print(cpr.mapping)
    print()
    code = cpr.codegen()
    with open(asmpath, "w") as f:
        f.write(code)
