# name: args count
from typing import List

from v_token import *

Commands = {
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
    def __init__(self, command: str, args: List[Token], label: str = ""):
        self.command: str = command
        self.args: List[Token] = args
        self.label: str = label

    def string(self):
        a = "[ "
        for arg in self.args:
            a += arg.data
        a += " ]"
        return "label: {label:20} | command: {command:20} | args: {args!r:20}".format(
            command=self.command,
            args=a,
            label=self.label
        )
