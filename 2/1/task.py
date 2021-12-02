import re


class Sub:

    command_re = re.compile("^(up|down|forward)\\s+(\\d+)$")

    def __init__(self):
        # x, y, z
        self._position = 0, 0, 0
        self._commands = {
            "up": self._up,
            "down": self._down,
            "forward": self._forward,
        }

    def _up(self, arg):
        x, y, z = self._position
        self._position = x, y, z - arg

    def _down(self, arg):
        x, y, z = self._position
        self._position = x, y, z + arg

    def _forward(self, arg):
        x, y, z = self._position
        self._position = x + arg, y, z

    def update(self, line):
        m = Sub.command_re.match(line)
        self._commands[m.group(1)](int(m.group(2)))

    def summary(self):
        x, y, z = self._position
        return x * z


sub = Sub()

with open("data.txt", "r") as f:
    for line in f:
        sub.update(line)

print(sub.summary())
        

