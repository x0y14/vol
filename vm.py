import time
from lexer import *
from parser import Parser
from v_operation import *


class VM:
    def __init__(self, path):
        self.program_path = path

        # memory
        self.mem = self.read_vol(path)
        self.mem_ops_mapping = {}

        # stack
        self.stack = []

        # program counter
        self.pc = 0

        # zero flag
        self.zf = 0

        # register
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0

    # stack pointer
    def sp(self) -> int:
        return len(self.stack) - 1

    def state(self, command, before=True):
        if before:
            print("VM.{:20} {{ reg_a: {:3}, reg_b: {:3}, reg_c: {:3}, pc: {:3}, zf: {} }}".format(
                command, self.reg_a, self.reg_b, self.reg_c, self.pc, self.zf), end="")
        else:
            print(" -> {{ reg_a: {:3}, reg_b: {:3}, reg_c: {:3}, pc: {:3}, zf: {} }}".format(
                self.reg_a, self.reg_b, self.reg_c, self.pc, self.zf))

    def mov_pc(self, n):
        self.pc += n

    def read_vol(self, path):
        with open(path, "r") as f:
            program = f.read()
        return lex(program)

    # def read_vol_as_ops(self, path) -> List[Operation]:
    #     with open(path, "r") as f:
    #         program = f.read()
    #     lx = Lexer(program)
    #     tokens = lx.lex()
    #     ps = Parser(tokens)
    #     return ps.parse()

    def mapping_ops(self):
        i = 0
        for op in self.mem_ops:
            if op.label != "":
                self.mem_ops_mapping[op.label] = i
            i += 1
        print(f"label-mapping : {self.mem_ops_mapping}")

    # def start_with_ops(self):
    #     self.state("start_with_ops")
    #     while True:
    #         op = self.mem_ops[self.pc]
    #         if op.command == "set_reg_a":
    #             n = op.args[0]
    #             self.reg_a = n
    #             self.mov_pc(1)
    #
    #         elif op.command == "set_reg_b":
    #             n = op.args[0]
    #             self.reg_b = n
    #             self.mov_pc(1)
    #
    #         elif op.command == "set_reg_c":
    #             n = op.args[0]
    #             self.reg_c = n
    #             self.mov_pc(1)
    #
    #         elif op.command == "add_b_to_a":
    #             self.add_b_to_a()
    #             self.mov_pc(1)
    #
    #         elif op.command == "add_c_to_a":
    #             self.add_c_to_a()
    #             self.mov_pc(1)
    #
    #         elif op.command == "compare_a_and_b":
    #             self.compare_a_and_b()
    #             self.mov_pc(1)
    #         elif op.command == "jump_eq":
    #             # print(op.string())
    #             # print(f"args: {op.args[0]}, addr: {self.mem_ops_mapping[op.args[0]]}")
    #             addr = self.mem_ops_mapping[op.args[0]]
    #             if self.zf == 1:
    #                 self.pc = addr
    #             else:
    #                 self.mov_pc(1)
    #
    #         elif op.command == "jump":
    #             addr = self.mem_ops_mapping[op.args[0]]
    #             self.pc = addr
    #
    #         elif op.command == "call":
    #             return_addr = self.pc + 1
    #             # set return_address
    #             self.reg_c = return_addr
    #
    #             addr_we_are_going = self.mem_ops_mapping[op.args[0]]
    #             # move
    #             self.pc = addr_we_are_going
    #         elif op.command == "ret":
    #             self.pc = self.reg_c
    #
    #         elif op.command == "exit":
    #             self.state(op.command)
    #             break
    #         else:
    #             raise Exception(f"Unknown command: {op.string()}")
    #         self.state(op.command)

    def start(self):
        print("vm:")
        while True:
            op = self.mem[self.pc]
            if op == "set_reg_a":
                self.state(op)
                n = self.mem[self.pc+1]
                self.reg_a = n
                self.pc += 2

            elif op == "set_reg_b":
                self.state(op)
                n = self.mem[self.pc+1]
                self.reg_b = n
                self.pc += 2

            elif op == "set_reg_c":
                self.state(op)
                n = self.mem[self.pc+1]
                self.reg_c = n
                self.pc += 2

            elif op == "add_b_to_a":
                self.state(op)
                self.add_b_to_a()
                self.pc += 1

            elif op == "add_c_to_a":
                self.state(op)
                self.add_c_to_a()
                self.pc += 1

            elif op == "compare_a_and_b":
                self.state(op)
                self.compare_a_and_b()
                self.pc += 1

            elif op == "jump_eq":
                self.state(op)
                addr = self.mem[self.pc + 1]
                if self.zf == 1:
                    self.pc = addr
                else:
                    self.pc += 2

            elif op == "jump":
                self.state(op)
                addr = self.mem[self.pc + 1]
                self.pc = addr

            elif op == "call":
                self.state(op)
                # 帰ってくる場所は、この命令の次の命令の部分。
                self.stack.append(self.pc + 2)
                addr_we_are_going = self.mem[self.pc + 1]
                self.pc = addr_we_are_going

            elif op == "ret":
                self.state(op)
                return_addr = self.stack.pop()
                self.pc = return_addr

            elif op == "exit":
                self.state(op)
                break
            else:
                raise f"Unknown operator({op})"

            self.state("", False)
            time.sleep(0.2)

    def set_mem(self, addr, n):
        self.mem[addr] = n

    def copy_mem_to_reg_a(self, addr):
        self.reg_a = self.mem[addr]

    def copy_mem_to_reg_b(self, addr):
        self.reg_b = self.mem[addr]

    def copy_reg_c_to_mem(self, addr):
        self.mem[addr] = self.reg_c

    def add_b_to_a(self):
        self.reg_a += self.reg_b

    def add_c_to_a(self):
        self.reg_a += self.reg_c

    def compare_a_and_b(self):
        if self.reg_a == self.reg_b:
            self.zf = 1
        else:
            self.zf = 0
