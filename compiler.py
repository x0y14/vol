import json
import sys
from pprint import pprint


class Compiler:
    def __init__(self):
        self.defined_variables = []
        self.defined_functions = {}

    def codegen(self, tree):
        asm_lines = ["call main", "exit"]

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

    def exchange_defined_variable(self, name_or_value):
        if name_or_value not in self.defined_variables:
            return name_or_value

        pos = self.defined_variables.index(name_or_value) + 1
        return f"[bp-{pos}]"

    def cdg_func_def(self, rest):
        asm_lines = []

        func_name = rest[0]
        if func_name in self.defined_functions:
            raise Exception(f"defined function: {func_name}")

        func_args = rest[1]
        # store how many arguments it have
        self.defined_functions[func_name] = len(func_args)

        func_body = rest[2]
        asm_lines.append("")
        asm_lines.append(f"\n{func_name}:")
        asm_lines.append(f"\t# 呼び出し元に戻れるように現状保存")
        asm_lines.append("\tpush bp")
        asm_lines.append(f"\tcp sp bp")

        if len(func_args) != 0:
            asm_lines.append(f"\n\t# 引数をローカル変数として代入")
        arg_no = 2
        for arg in func_args:
            # 引数をローカル変数へと変換。
            self.defined_variables.append(arg)
            arg_as_local_value_pos = self.defined_variables.index(arg) + 1
            asm_lines.append(f"\t# {arg}")
            asm_lines.append(f"\tsub_sp 1")
            asm_lines.append(f"\tcp [bp+{arg_no}] [bp-{arg_as_local_value_pos}]")
            arg_no += 1

        asm_lines.append(f"\t# todo : 関数本体")
        for stmt in func_body:
            stmt_head, stmt_rest = stmt[0], stmt[1:]
            asm_lines.append("")

            if stmt_head == "call":
                func_name = stmt_rest[0]
                # if func_name not in self.defined_functions:
                #     raise Exception(f"undefined function: {func_name}")
                func_args: list = stmt_rest[1]
                # if len(func_args) != self.defined_functions[func_name]:
                #     raise Exception(f"dose not match number of function arguments: {func_name}")
                if type(func_args) is list and len(func_args) != 0:
                    # has args; 逆順にpush
                    func_args.reverse()
                    for arg in func_args:
                        # 変数を変換して入れる
                        arg_candidate = self.exchange_defined_variable(arg)
                        if arg_candidate is None:
                            asm_lines.append(f"\tpush {arg} # 引数")
                        else:
                            asm_lines.append(f"\tpush {arg_candidate} # 引数({arg})")

                    asm_lines.append(f"\tcall {func_name} # 関数呼び出し")
                    # sp戻す。
                    asm_lines.append(f"\tadd_sp {len(func_args)} # 呼び出し後の位置修正")

                else:
                    asm_lines.append(f"\tcall {func_name} # 関数呼び出し")

            elif stmt_head == "call_set":
                define_return_value = stmt_rest[0]
                func_rest = stmt_rest[1]

                func_name = func_rest[0]
                func_args: list = func_rest[1]

                if type(func_args) is list and len(func_args) != 0:
                    # has args; 逆順にpush
                    func_args.reverse()
                    for arg in func_args:
                        # 変数を変換して入れる
                        arg_candidate = self.exchange_defined_variable(arg)
                        if arg_candidate is None:
                            asm_lines.append(f"\tpush {arg} # 引数")
                        else:
                            asm_lines.append(f"\tpush {arg_candidate} # 引数({arg})")

                    asm_lines.append(f"\tcall {func_name} # 関数呼び出し")
                    # sp戻す。
                    asm_lines.append(f"\tadd_sp {len(func_args)} # 呼び出し後の位置修正")

                else:
                    asm_lines.append(f"\tcall {func_name} # 関数呼び出し")

                asm_lines.append("\t# 戻り値をローカル変数に格納")
                pos = self.defined_variables.index(define_return_value) + 1
                asm_lines.append(f"\tcp reg_a [bp-{pos}]")

            elif stmt_head == "var":
                self.defined_variables.append(stmt_rest[0])
                asm_lines.append(f"\t# 引数準備 : {stmt_rest[0]}")
                asm_lines.append(f"\tsub_sp 1")

            elif stmt_head == "set":
                # print(stmt_rest)
                value_def_name = stmt_rest[0]  # name
                value_data = stmt_rest[1]  # value

                asm_lines.append(f"\t# ローカル変数に値を代入")

                # value = self.exchange_defined_variable(value_def_name)
                # if value is None:
                #     value = value_data

                # int
                if type(value_data) is int:
                    value = value_data
                    pos = self.defined_variables.index(value_def_name)+1
                    asm_lines.append(f"\tcp {value} [bp-{pos}]")
                # str
                elif (type(value_data) is str) and (value_data[0] == "\"" and value_data[-1] == "\""):
                    value = value_data
                    pos = self.defined_variables.index(value_def_name)+1
                    asm_lines.append(f"\tcp {value} [bp-{pos}]")
                # defined keyword
                elif value_data in self.defined_variables:
                    pos = self.defined_variables.index(value_def_name)+1
                    value = self.exchange_defined_variable(value_data)
                    asm_lines.append(f"\tcp {value} [bp-{pos}]")
                else:
                    raise Exception(f"not yet impl: {stmt_rest}")

            elif stmt_head == "return":
                return_value = stmt_rest[0][0]
                if return_value[0] == "[" and return_value[-1] == "]":
                    v = self.exchange_defined_variable(return_value)
                    if v is None:
                        raise Exception(f"undefined variable: {return_value}")
                    else:
                        return_value = v

                asm_lines.append("\n\t# 戻り値を設定")
                asm_lines.append(f"\tcp {return_value} reg_a")

            elif stmt_head == "print":
                value_or_keyword = stmt_rest[0]

                if type(value_or_keyword) is int:
                    # this is int
                    asm_lines.append(f"\techo {value_or_keyword}")
                elif type(value_or_keyword) is str and (value_or_keyword[0] == "\"" and value_or_keyword[-1] == "\""):
                    # this is str
                    asm_lines.append(f"\techo {value_or_keyword}")
                elif type(value_or_keyword) is str and (value_or_keyword in self.defined_variables):
                    # this is keyword
                    pos = self.defined_variables.index(value_or_keyword)+1
                    asm_lines.append(f"\techo [bp-{pos}]")
                else:
                    raise Exception(f"not yet impl: {stmt_rest}")

            else:
                raise Exception(f"not yet impl: {stmt_head}")

        asm_lines.append(f"\n\t# 現状復帰")
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
