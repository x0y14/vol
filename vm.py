import re
import time

from lexer import *
from parser import Parser
from v_command import Commands
from v_operation import *
from memory import *


class VM:
    def __init__(self, path, mem: Memory):
        self.program_path = path

        # memory
        self.mem = mem
        self.mem.main.extend(self.read_vol(path))

        # stack
        # self.mem.stack

        # program counter
        self.pc = 0
        # base pointer
        self.bp = len(self.mem.main) - 1
        # stack pointer
        self.sp = len(self.mem.stack) - 1

        # zero flag
        self.zf = 0

        # register
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0

        self.display_lines = 0
        self.display = []

    def mov_pc(self, n):
        self.pc += n

    def read_vol(self, path):
        with open(path, "r") as f:
            program = f.read()
        return lex(program)

    def start(self, step_debug=False, use_display=False):
        if step_debug:
            print("Step Debug >> Press enter to next step")
        print(f"VM {{ ST-Debug: {step_debug}, Display: {use_display} }}:\n")
        while True:
            print("=== Display ===")
            print(self.display)
            print("\033[2A")

            self.mem.dump(
                regs=[self.reg_a, self.reg_b, self.reg_c],
                pc=self.pc,
                zf=self.zf,
                bp=self.bp,
                sp=self.sp)

            op = self.mem.main[self.pc]
            if op == "set_reg_a":
                # self.state(op)
                n = self.mem.main[self.pc + 1]
                self.reg_a = n
                self.pc += 2

            elif op == "set_reg_b":
                # self.state(op)
                n = self.mem.main[self.pc + 1]
                self.reg_b = n
                self.pc += 2

            elif op == "set_reg_c":
                # self.state(op)
                n = self.mem.main[self.pc + 1]
                self.reg_c = n
                self.pc += 2

            elif op == "add_b_to_a":
                # self.state(op)
                self.add_b_to_a()
                self.pc += 1

            elif op == "add_c_to_a":
                # self.state(op)
                self.add_c_to_a()
                self.pc += 1

            elif op == "add":
                operand1 = self.mem.main[self.pc + 1]
                val = self.mem.main[self.pc + 2]
                data = self.convert_keyword(val)

                if operand1 == "reg_a":
                    self.reg_a += data
                elif operand1 == "reg_b":
                    self.reg_b += data
                elif operand1 == "reg_c":
                    self.reg_c += data

                self.pc += 3

            elif op == "sub":
                operand1 = self.mem.main[self.pc + 1]
                val = self.mem.main[self.pc + 2]
                data = self.convert_keyword(val)

                if operand1 == "reg_a":
                    self.reg_a -= data
                elif operand1 == "reg_b":
                    self.reg_b -= data
                elif operand1 == "reg_c":
                    self.reg_c -= data

                self.pc += 3

            elif op == "cmp":
                operand1 = self.mem.main[self.pc + 1]
                operand2 = self.mem.main[self.pc + 2]
                if self.convert_keyword(operand1) == self.convert_keyword(operand2):
                    self.zf = 1
                else:
                    self.zf = 0
                self.pc += 3

            elif op == "compare_a_and_b":
                # self.state(op)
                self.compare_a_and_b()
                self.pc += 1

            elif op == "jump_eq":
                # self.state(op)
                addr = self.mem.main[self.pc + 1]
                if self.zf == 1:
                    self.pc = addr
                else:
                    self.pc += 2

            elif op == "jump":
                # self.state(op)
                addr = self.mem.main[self.pc + 1]
                self.pc = addr

            # jump if zero
            elif op == "jz":
                if self.zf == 0:
                    addr = self.mem.main[self.pc + 1]
                    self.pc = addr
                else:
                    self.pc += 2
            # jump if not zero
            elif op == "jnz":
                if self.zf != 0:
                    addr = self.mem.main[self.pc + 1]
                    self.pc = addr
                else:
                    self.pc += 2

            elif op == "call":
                # self.state(op)
                # 帰ってくる場所は、この命令の次の命令の部分。
                self.add_sp(-1)
                self.mem.stack[self.sp] = self.pc + 2
                addr_we_are_going = self.mem.main[self.pc + 1]
                self.pc = addr_we_are_going

            elif op == "ret":
                return_addr = self.mem.stack[self.sp]
                self.add_sp(1)
                self.pc = return_addr

            # elif op == "copy_bp_to_sp":
            #     self.sp = self.bp
            #     self.pc += 1
            # elif op == "copy_sp_to_bp":
            #     self.bp = self.sp
            #     self.pc += 1
            elif op == "cp":
                from_ = self.mem.main[self.pc + 1]
                to_ = self.mem.main[self.pc + 2]
                self.cpy(from_, to_)
                self.pc += 3

            elif op == "push":
                arg = self.mem.main[self.pc + 1]
                # keyword
                if arg in ["reg_a", "reg_b", "reg_c", "bp", "sp"]:
                    data = self.convert_keyword(arg)
                # numeric
                elif type(arg) is int or type(arg) is float:
                    data = arg
                # string
                elif (arg[0] == "\"" and arg[-1] == "\"") or arg[0] == "\'" and arg[-1] == "\'":
                    data = arg
                else:
                    raise Exception(f"push: not ye implemented ({arg})")

                self.add_sp(-1)
                self.mem.stack[self.sp] = data
                self.pc += 2
            elif op == "pop":
                arg = self.mem.main[self.pc + 1]
                if arg == "bp":
                    self.bp = self.mem.stack[self.sp]
                elif arg == "sp":
                    self.set_sp(self.mem.stack[self.sp])
                elif arg == "reg_a":
                    self.reg_a = self.mem.stack[self.sp]
                elif arg == "reg_b":
                    self.reg_b = self.mem.stack[self.sp]
                elif arg == "reg_c":
                    self.reg_c = self.mem.stack[self.sp]
                else:
                    raise Exception(f"push: not ye implemented ({arg})")

                self.add_sp(1)
                self.pc += 2

            elif op == "add_sp":
                arg = self.mem.main[self.pc + 1]
                self.add_sp(arg)
                self.pc += 2

            elif op == "sub_sp":
                arg = self.mem.main[self.pc + 1]
                self.sub_sp(arg)
                self.pc += 2

            elif op == "echo":
                letters = self.mem.main[self.pc + 1]
                data = str(letters)
                if letters == "reg_a":
                    data = str(self.reg_a)
                elif letters == "reg_b":
                    data = str(self.reg_b)
                elif letters == "reg_c":
                    data = str(self.reg_c)
                self.echo(data)
                self.pc += 2

            elif op == "exit":
                break
            else:
                raise Exception(f"Unknown operator `{op}`")

            if step_debug:
                input()
            else:
                time.sleep(0.2)

    def cpy(self, from_, to_):
        if from_ == "bp":
            val = self.bp
        elif from_ == "sp":
            val = self.sp
        elif (from_[0] == "[") and (from_[-1] == "]"):
            val = self.addr_convert(from_)
        else:
            raise Exception(f"cpy: unknown src value({from_})")

        if to_ == "bp":
            self.bp = val
        elif to_ == "sp":
            self.set_sp(val)
        elif to_ == "reg_a":
            self.reg_a = val
        elif to_ == "reg_b":
            self.reg_b = val
        elif to_ == "reg_c":
            self.reg_c = val
        # elif (to_[0] == "[") and (to_[-1] == "]"):
        #     self.addr_convert(to_)
        else:
            raise Exception(f"cpy: unknown dest value({from_})")

    def addr_convert(self, addr):
        # addr: "[bp+1]" -> return self.bp + 1
        addr_reg = re.compile(r"\[(bp|sp)([+\-])(\d+)]")
        match = addr_reg.match(addr)
        bp_sp = match.group(1)
        plus_minus = match.group(2)
        val = int(match.group(3))

        # # target
        if bp_sp == "bp":
            if plus_minus == "+":
                return self.mem.stack[self.bp + val]
            elif plus_minus == "-":
                return self.mem.stack[self.bp - val]
            else:
                raise Exception(f"cpy: no impl({addr})")
        else:
            raise Exception(f"cpy: no impl({addr})")

    def convert_keyword(self, keyword):
        reserved = ["reg_a", "reg_b", "reg_c", "bp", "sp"]
        if keyword not in reserved:
            raise Exception(f"convert_keyword: unknown({keyword})")

        if keyword == "reg_a":
            return self.reg_a

        if keyword == "reg_b":
            return self.reg_b

        if keyword == "reg_c":
            return self.reg_c

        if keyword == "bp":
            return self.bp

        if keyword == "sp":
            return self.sp

    def set_sp(self, n):
        if n < 0:
            raise Exception("stack over flow")
        self.sp = n

    def add_sp(self, n):
        if (self.sp + n) < 0:
            raise Exception("stack over flow")
        self.sp += n

    def sub_sp(self, n):
        if (self.sp - n) < 0:
            raise Exception("stack over flow")
        self.sp -= n

    def echo(self, letters):
        self.display.append(letters)

    def set_mem(self, addr, n):
        self.mem.main[addr] = n

    def copy_mem_to_reg_a(self, addr):
        self.reg_a = self.mem.main[addr]

    def copy_mem_to_reg_b(self, addr):
        self.reg_b = self.mem.main[addr]

    def copy_reg_c_to_mem(self, addr):
        self.mem.main[addr] = self.reg_c

    def add_b_to_a(self):
        self.reg_a += self.reg_b

    def add_c_to_a(self):
        self.reg_a += self.reg_c

    def compare_a_and_b(self):
        if self.reg_a == self.reg_b:
            self.zf = 1
        else:
            self.zf = 0
