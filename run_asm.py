import sys
from vm import VM
from code_gen import CodeGenerator
from memory import *


def main():
    # prepare compiler
    asm_path = sys.argv[1]

    # prepare virtual machine
    # - create memory
    mem_size = 20
    mem = Memory(mem_size, [], {})
    # init
    vm = VM(asm_path, mem)

    # lunch
    vm.start(step_debug=True, use_display=True)


if __name__ == '__main__':
    main()
