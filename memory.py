from v_command import *
import sys


class Memory:
    def __init__(self, mid: dict, label_mapping: dict):
        # main memory
        self.main = []
        self.mid = mid
        self.mapping = label_mapping

        # stack
        self.stack = []

    def dump(self, regs, zf, sp, pc):
        l0 = self.dump_vm(regs, zf, sp)
        l1, is_exit = self.dump_main(pc)
        l2 = self.dump_stack()
        if not is_exit:
            print(f"\033[{l0+l1+l2}A", end="")
        else:
            print()

    def dump_vm(self, regs, zf, sp):
        print("=== VM ===")
        s = {"reg": {"a": regs[0], "b": regs[1], "c": regs[2]}, "zf": zf}
        print(f"\033[2K\033[G{str(s)}", end="")
        return 2

    def dump_main(self, pc: int) -> (int, bool):
        print()
        print("=== Memory (main) ===")
        status = ""
        is_exit = False
        for mid_line in self.mid:
            arrow = ""
            if pc == mid_line['pc']:
                arrow = "-->"
                if mid_line['raw'] == ['exit']:
                    is_exit = True
                else:
                    is_exit = False
            status += "{:3} | {:3} | {:30}\n".format(arrow, mid_line['pc'], self.cmd_coloring(mid_line['raw']))

        print(status, end="")

        # if not is_exit:
        #     print(f"\033[{len(self.mid)+2}A", end="")
        return len(self.mid)+1, is_exit

    def cmd_coloring(self, cmd) -> str:
        if cmd[0] in ["call", "ret", "jump", "jump_eq"]:
            # 34, 221, 242
            # return f"\033[34m{str(cmd)}\033[0m"
            if cmd[0] == "ret":
                return f"\033[34m{str(cmd)}\033[0m"
            else:
                return f"\033[34m{str(cmd)}\033[0m => {self.mapping[cmd[1]]}"
        if cmd[0] == "exit":
            return f"\033[07m{str(cmd)}\033[0m"
        if "set_reg" in cmd[0]:
            return f"\033[32m{str(cmd)}\033[0m"
        return str(cmd)

    def dump_stack(self) -> int:
        print("=== Memory (stack) ===")
        # print("[".format())
        print(f"\033[2K\033[G{str(self.stack)}", end="")
        # print("\r", end="")
        # stack_no = 0
        # for s in self.stack:
        #     print("{}, ".format(s), end="")
        #     stack_no += 1
        # print(" ]")
        return 2