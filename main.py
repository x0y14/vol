import sys
from vm import VM
from code_gen import CodeGenerator
from memory import *


def main():
    # prepare compiler
    in_filepath = sys.argv[1]
    asm_out_path = sys.argv[2]
    cgen = CodeGenerator(in_filepath)
    cgen.convert()
    cgen.mem_mapping()
    code = cgen.codegen()
    with open(asm_out_path, "w") as f:
        f.write(code)
    mid = cgen.mid
    label_mapping = cgen.mapping

    # prepare virtual machine
    # - create memory
    mem_size = 20
    mem = Memory(mem_size, mid, label_mapping)
    # init
    vm = VM(asm_out_path, mem)

    # lunch
    vm.start(step_debug=True, use_display=True)


if __name__ == '__main__':
    main()
