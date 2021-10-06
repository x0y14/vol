import sys
from vm import VM
from compiler import Compiler
from memory import *


def main():
    # prepare compiler
    filepath = sys.argv[1]
    asm_path = sys.argv[2]
    cpr = Compiler(filepath)
    cpr.convert()
    cpr.mem_mapping()
    code = cpr.codegen()
    with open(asm_path, "w") as f:
        f.write(code)

    # prepare virtual machine
    # - create memory
    mem = Memory()
    vm = VM(asm_path, mem)
    vm.start()


if __name__ == '__main__':
    main()
