from vm import VM


def main():
    vm = VM()

    vm.set_mem(0, 1)
    vm.set_mem(1, 2)
    vm.state()

    vm.copy_mem_to_reg_a(0)
    vm.copy_mem_to_reg_b(1)
    vm.state()

    vm.add_ab()
    vm.copy_reg_c_to_mem(2)
    vm.state()


if __name__ == '__main__':
    main()
