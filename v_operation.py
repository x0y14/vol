from typing import List


class Operation:
    def __init__(self, command: str, args: List, label: str = ""):
        self.command: str = command
        self.args: List = args
        self.label: str = label

    def string(self):
        a = "[ "
        for arg in self.args:
            a += str(arg)
        a += " ]"
        return "label: {label:20} | command: {command:20} | args: {args!r:20}".format(
            command=self.command,
            args=a,
            label=self.label
        )
