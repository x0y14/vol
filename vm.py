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

        # stack pointer
        self.sp = 0

        # zero flag
        self.zf = 0

        # register
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0

    def mov_pc(self, n):
        self.pc += n

    def read_vol(self, path):
        with open(path, "r") as f:
            program = f.read()
        return lex(program)

    def start(self, step_debug=False):
        if step_debug:
            print("Step Debug >> Press enter to next step")
        print("vm:\n")
        while True:
            self.mem.dump(
                regs=[self.reg_a, self.reg_b, self.reg_c],
                pc=self.pc,
                zf=self.zf,
                sp=self.sp)

            op = self.mem.main[self.pc]
            if op == "set_reg_a":
                # self.state(op)
                n = self.mem.main[self.pc+1]
                self.reg_a = n
                self.pc += 2

            elif op == "set_reg_b":
                # self.state(op)
                n = self.mem.main[self.pc+1]
                self.reg_b = n
                self.pc += 2

            elif op == "set_reg_c":
                # self.state(op)
                n = self.mem.main[self.pc+1]
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

            elif op == "call":
                # self.state(op)
                # 帰ってくる場所は、この命令の次の命令の部分。
                self.mem.stack.append(self.pc + 2)
                self.sp += 1
                addr_we_are_going = self.mem.main[self.pc + 1]
                self.pc = addr_we_are_going

            elif op == "ret":
                # self.state(op)
                return_addr = self.mem.stack.pop()
                self.sp -= 1
                self.pc = return_addr

            elif op == "exit":
                # self.state(op)
                break
            else:
                raise f"Unknown operator({op})"

            if step_debug:
                input()
            else:
                time.sleep(0.2)

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
