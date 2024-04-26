from Node import Node
from Command_Expression import Command_Expression


class Program_Expression(Node):
    def __init__(self, commands):
        self.commands = commands

    def nodes(self):
        return self.commands

    @classmethod
    def construct(cls, parser):
        commands = []

        while True:
            if parser.next().of("EOF"):
                break
            command = Command_Expression.construct(parser)
            commands.append(command)

        return Program_Expression(commands)
