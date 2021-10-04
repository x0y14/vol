# name: args count
commands = {
    "set_reg_a": 1,
    "set_reg_b": 1,
    "set_reg_c": 1,

    "add_b_to_a": 1,
    "add_c_to_a": 1,

    "compare_a_and_b": 0,

    "jump": 1,
    "jump_eq": 1,

    "exit": 0,
}


class Operation:
    def __init__(self, command: str, args, label=""):
        self.command = command
        self.args = args,
        self.label = label
