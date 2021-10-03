from vm import VM


def main():
    vm = VM("./program.vol")
    vm.state()
    vm.start()


if __name__ == '__main__':
    main()
