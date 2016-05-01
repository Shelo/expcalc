#!/usr/bin/env python
import os

import calc
import sys


class CalculatorTerminalController(object):
    def __init__(self):
        self.daemon = True
        self.calc = calc.Calculator()

    def begin(self):
        while self.daemon:
            _input = raw_input()

            out = self.calc.execute(_input)

            if out[0] == '[':
                print "\033[93m" + out + "\033[0m"


def get_build_number():
    path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(path, ".buildc"), "r+") as buildc:
        c = int(buildc.read())
        buildc.seek(0)
        buildc.truncate()
        buildc.write(str(c + 1))
        return c


if __name__ == '__main__':
    print "Expression Calculator b.%d - Marcelo Jara A." % get_build_number()
    print

    try:
        ctrl = CalculatorTerminalController()
        ctrl.begin()
    except KeyboardInterrupt:
        print "\nGoodbye!"
        sys.exit(0)
