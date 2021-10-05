import sys
from vm import VM
from compiler import Compiler


def main():
    filepath = sys.argv[1]
    asm_path = sys.argv[2]
    cpr = Compiler(filepath)
    cpr.convert()
    cpr.mem_mapping()
    code = cpr.codegen()
    with open(asm_path, "w") as f:
        f.write(code)

    # exec
    vm = VM(asm_path)
    vm.start()


if __name__ == '__main__':
    main()
