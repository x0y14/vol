import json
import sys
from pprint import pprint


class Compiler:
    def __init__(self):
        pass

    def codegen(self, tree):
        asm_lines = ["call main", "exit", ""]

        head, rest = tree[0], tree[1:]
        if head != "stmts":
            raise Exception(f"[codegen] not impl : {head}")
        asm_lines = [*asm_lines, *self.cdg_stmts(rest)]

        return asm_lines

    def cdg_stmts(self, rest):
        asm_lines = []

        for stmt in rest:
            stmts_head, stmts_rest = stmt[0], stmt[1:]
            if stmts_head == "func":
                asm_lines = [*asm_lines, *self.cdg_func_def(stmts_rest)]
            else:
                raise Exception(f"[cdg_stmts] not yet impl : {stmts_head}")

        return asm_lines

    def cdg_func_def(self, rest):
        asm_lines = []

        func_name = rest[0]
        # func_values = tree[1]?
        func_body = rest[2]

        asm_lines.append(f"{func_name}:")
        asm_lines.append("\tpush bp")
        asm_lines.append(f"\tcp sp bp")

        asm_lines.append(f"\t# todo : 関数本体")
        for stmt in func_body:
            stmt_head, stmt_rest = stmt[0], stmt[1:]

            if stmt_head == "call":
                func_name = stmt_rest[0]
                # func_args = stmt_rest[1]
                asm_lines.append(f"\tcall {func_name}")
            else:
                raise Exception(f"not yet impl: {stmt_head}")

        asm_lines.append(f"\tcp bp sp")
        asm_lines.append(f"\tpop bp")
        asm_lines.append(f"\tret")
        asm_lines.append("")

        return asm_lines


def export(asm_lines, output):
    a = ""
    for al in asm_lines:
        a += al + "\n"
    with open(output, "w") as f:
        f.write(a)


if __name__ == "__main__":
    filepath = sys.argv[1]
    output_path = sys.argv[2]
    cpr = Compiler()

    with open(filepath, "r") as f:
        src = f.read()

    t = json.loads(src)
    pprint(t)
    asm = cpr.codegen(t)

    export(asm, output_path)

