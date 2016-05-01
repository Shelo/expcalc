import imp

from lexer import ExpressionLexer
import os
import math

userdefs = {}


class Calculator(object):
    MAX_INPUT = 256

    def __init__(self):
        self.lexer = ExpressionLexer()

        self.history = []
        self.logs = []
        self.exps = {}

        self.commands = {
            'let': self._cmd_let,
            'out': self._cmd_out,
            'exp': self._cmd_exp,
        }

        self.execute("let pi = " + str(math.pi))
        self.execute("let g = 9.81")
        self.execute("let e = " + str(math.e))

        self.user_home = os.path.expanduser('~')
        self.user_defs = os.path.join(self.user_home, ".expcalc.py")
        self._load_home_userdefs()

    def execute(self, _input):
        assert len(_input) < self.MAX_INPUT

        self.history.append(_input)

        log_length = len(self.logs)

        self._process(_input)

        # all commands should log something.
        if len(self.logs) <= log_length:
            return "Command did not log any message"
        else:
            return self.logs[-1]

    def _process(self, _input):
        tokens = self.lexer.parse(_input)

        cmd = tokens[0].lexeme

        if cmd in self.commands:
            try:
                self.commands[cmd](tokens[1:])
            except ValueError as e:
                self._log("[err] %s", e.message)
        else:
            try:
                self._log("[%s] %.5f", _input, self._process_calc(tokens))
            except ValueError:
                self._log("[err] Command '%s' does not exists", cmd)
            except ZeroDivisionError:
                self._log("[err] division by zero")

    def _replace_exp(self, expression):
        final_exp = []

        for i, t in enumerate(expression):
            if t.type == ExpressionLexer.TAG_IDENTIFIER:
                self._assert_token_exists(t)

                # in this case, get the result and replace it in the
                # expression.
                var_value = self.exps[t]
                result = self._process_calc(var_value)
                # expression[i] = result
                final_exp.append(result)

            elif t.type == ExpressionLexer.TAG_NUMBER:
                final_exp.append(float(t.lexeme))

            elif t.type == ExpressionLexer.TAG_FUNCTION:
                final_exp.append("userdefs." + t.lexeme)

            else:
                final_exp.append(t.lexeme)

        return final_exp

    def _process_calc(self, expression):
        expression = list(expression)
        expression = self._replace_exp(expression)
        return eval(" ".join(map(str, expression)))

    def _cmd_let(self, tokens):
        """
        Registers an expression name and value.
        """
        self._assert_min_length(tokens, 3)
        self._assert_is(tokens[1], '=')

        exp_name = tokens[0]
        exp_value = tokens[2:]

        self.exps[exp_name] = exp_value

        self._log("Set %s to %s", exp_name, exp_value)

    def _cmd_out(self, tokens):
        """
        Resolves an expression given the name.
        """
        self._assert_length(tokens, 1)

        # validate the existence of the expression.
        exp_name = tokens[0]
        self._assert_token_exists(exp_name)

        # retrieve the result.
        result = self._process_calc(self.exps[exp_name])

        # log the result.
        self._log("[%s] %.5f", tokens[0].lexeme, result)

    def _cmd_exp(self, tokens):
        """
        Logs the expression of a given name.
        """
        self._assert_length(tokens, 1)

        # validate the existence of the expression.
        exp_name = tokens[0]
        self._assert_token_exists(exp_name)

        self._log("[%s] %s", tokens[0], " ".join(self.exps[exp_name]))

    def _log(self, message, *args):
        self.logs.append(message % args)

    def _load_home_userdefs(self):
        global userdefs

        if not os.path.exists(self.user_defs):
            self._create_userdefs()

        userdefs = imp.load_source('userdefs', self.user_defs)

    def _create_userdefs(self):
        with open(self.user_defs, "w") as user_defs:
            user_defs.write("from math import *")

    @staticmethod
    def _assert_length(tokens, length):
        if len(tokens) != length:
            raise ValueError("command must have %d tokens" % length)

    @staticmethod
    def _assert_min_length(tokens, length):
        if len(tokens) < length:
            raise ValueError("command must have at least %d tokens" % length)

    @staticmethod
    def _assert_is(token, should):
        if token.lexeme != should:
            raise ValueError("token is %s, but must be %s" % (token, should))

    def _assert_token_exists(self, var_name):
        if var_name not in self.exps:
            raise ValueError("undefined %s" % var_name)
