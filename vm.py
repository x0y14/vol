from misc import *


class VM:
    def __init__(self):
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0
        self.mem = [
            "set_reg_a", 1,
            "set_reg_a", 0,
        ]

    def state(self):
        print(f"VM {{ reg_a: {self.reg_a}, reg_b: {self.reg_b}, reg_c: {self.reg_c}, mem: {self.mem} }}")

    def set_mem(self, addr, n):
        self.mem[addr] = n

    def copy_mem_to_reg_a(self, addr):
        self.reg_a = self.mem[addr]

    def copy_mem_to_reg_b(self, addr):
        self.reg_b = self.mem[addr]

    def copy_reg_c_to_mem(self, addr):
        self.mem[addr] = self.reg_c

    def add_ab(self):
        self.reg_c = self.reg_a + self.reg_b
