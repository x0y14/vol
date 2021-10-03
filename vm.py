import time

from misc import *


class VM:
    def __init__(self):
        # program counter
        self.pc = 0

        # register
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0

        # memory
        self.mem = [
            "set_reg_a", 0,
            "set_reg_b", 1,
            "add_b_to_a",
            "jump", 4,
            "exit",
        ]

    def state(self):
        print(f"VM {{ reg_a: {self.reg_a}, reg_b: {self.reg_b}, reg_c: {self.reg_c}, mem: {self.mem} }}, pc: {self.pc}")

    def start(self):
        while True:
            op = self.mem[self.pc]
            if op == "set_reg_a":
                n = self.mem[self.pc+1]
                self.reg_a = n
                self.pc += 2

            elif op == "set_reg_b":
                n = self.mem[self.pc+1]
                self.reg_b = n
                self.pc += 2

            elif op == "add_b_to_a":
                self.add_b_to_a()
                self.pc += 1

            elif op == "jump":
                addr = self.mem[self.pc + 1]
                self.pc = addr

            elif op == "exit":
                print("VM exit")
                break
            else:
                raise f"Unknown operator({op})"

            self.state()
            time.sleep(0.5)

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
