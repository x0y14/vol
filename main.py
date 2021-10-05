import sys
from vm import VM


def main():
    filepath = sys.argv[1]
    # todo : compiler

    # exec
    vm = VM(filepath)
    vm.start_with_ops()


if __name__ == '__main__':
    main()
