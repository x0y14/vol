import sys
from vm import VM
from mid_compiler import MidCompiler
from memory import *


def main():
    # prepare compiler
    filepath = sys.argv[1]
    asm_path = sys.argv[2]
    cpr = MidCompiler(filepath)
    cpr.convert()
    cpr.mem_mapping()
    code = cpr.codegen()
    with open(asm_path, "w") as f:
        f.write(code)
    mid = cpr.mid
    label_mapping = cpr.mapping

    # prepare virtual machine
    # - create memory
    mem_size = 20
    mem = Memory(mem_size, mid, label_mapping)
    # init
    vm = VM(asm_path, mem)

    # lunch
    vm.start(step_debug=True, use_display=True)


if __name__ == '__main__':
    main()
