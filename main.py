#!/usr/bin/env python

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


if __name__ == '__main__':
    print "Expression Calculator b.0005 - Marcelo Jara Almeyda"
    print "=============================================="

    try:
        ctrl = CalculatorTerminalController()
        ctrl.begin()
    except KeyboardInterrupt:
        print "\nGoodbye!"
        sys.exit(0)

    """
    calc = extcalc.Calculator()
    print calc.execute("let y = 4.5")
    print calc.execute("let x = 3 + y")
    print calc.execute("out x")
    print calc.execute("let y = 9.81")
    print calc.execute("out x")
    """
