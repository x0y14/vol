import sys
from pprint import pprint

from lexer import *
from parser import *


class CodeGenerator:
    def __init__(self, path):
        self.filepath = path

        with open(path, "r") as f:
            program = f.read()

        lxr = Lexer(program)
        psr = Parser(lxr.lex())
        self.ops = psr.parse()

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

    def convert(self):
        lines = []
        op_pc = 0
        for op in self.ops:
            lines.append({"label": op.label, "raw": [op.command, *op.args], "pc": op_pc})
            op_pc += 1 + len(op.args)

        self.mid = lines
        print("cpr-mid:")
        pprint(self.mid)
        print()

    def codegen(self) -> str:
        asm = ""
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

            asm += line + "\n"
            line = ""

        return asm


if __name__ == "__main__":
    filepath = sys.argv[1]
    asm_path = sys.argv[2]
    cpr = CodeGenerator(filepath)
    cpr.convert()
    cpr.mem_mapping()
    code = cpr.codegen()
    with open(asm_path, "w") as f:
        f.write(code)
