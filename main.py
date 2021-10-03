import sys
from vm import VM


def main():
    filepath = sys.argv[1]
    vm = VM(filepath)
    vm.start()


if __name__ == '__main__':
    main()
