from math import *


class Token(object):
    def __init__(self, lexeme, _type):
        self.lexeme = lexeme
        self.type = _type

    def __str__(self):
        return "[%d] %s" % (self.type, self.lexeme)


class ExpressionLexer(object):
    TAG_LET = 301
    TAG_OUT = 302
    TAG_NUMBER = 303
    TAG_IDENTIFIER = 304
    TAG_FUNCTION = 305

    def __init__(self):
        self.words = {}
        self.symbols = {}

        self.cursor = None
        self.peek = None
        self.input = None

        self._reserve(Token("let", self.TAG_LET))
        self._reserve(Token("out", self.TAG_OUT))

        self._reserve_symbol('+')
        self._reserve_symbol('-')
        self._reserve_symbol('/')
        self._reserve_symbol('*')
        self._reserve_symbol('=')
        self._reserve_symbol('^')
        self._reserve_symbol('(')
        self._reserve_symbol(')')
        self._reserve_symbol(',')

    def parse(self, _input):
        self.input = _input
        self.peek = ' '
        self.cursor = 0

        tokens = []
        while self.cursor < len(self.input) or self.peek != ' ':
            tokens.append(self.scan())

        return tokens

    def scan(self):
        while True:
            if self.peek.isspace():
                self._next_char()
                continue
            else:
                break

        if self.peek in self.symbols:
            token = self.symbols[self.peek]
            self._next_char()
            return token

        if self.peek.isdigit():
            # [0-9]+
            captured = self.peek
            while self._next_char() and self.peek.isdigit():
                captured += self.peek

            if self.peek == '.':
                captured += self.peek

                while self._next_char() and self.peek.isdigit():
                    captured += self.peek

            return Token(captured, self.TAG_NUMBER)

        if self.peek.isalpha():
            # [a-zA-Z][0-9a-zA-Z]*
            captured = self.peek
            while self._next_char() and self.peek.isalnum():
                captured += self.peek

            if self.peek == '(':
                # this is a function call.
                captured += self.peek
                self._next_char()
                return Token(captured, self.TAG_FUNCTION)

            if captured not in self.words:
                self.words[captured] = Token(captured, self.TAG_IDENTIFIER)

            return self.words[captured]

        raise ValueError("Invalid String")

    def _next_char(self):
        if self.cursor >= len(self.input):
            self.peek = ' '
            return False

        self.peek = self.input[self.cursor]
        self.cursor += 1
        return True

    def _next_char_is(self, cmp):
        self._next_char()

        if self.peek != cmp:
            return False

        # TODO: not sure why...
        self.peek = ' '
        return True

    def _reserve(self, token):
        # type: (Token) -> None
        self.words[token.lexeme] = token

    def _reserve_symbol(self, symbol):
        self.symbols[symbol] = Token(symbol, ord(symbol))


"""
def debug_tokens(tokens):
    print " ".join([token.lexeme for token in tokens])


def exp_call_match(tokens):
    opens = 1

    for i, token in enumerate(tokens):
        if token.type == ord('('):
            opens += 1
        elif token.type == ExpressionLexer.TAG_FUNCTION:
            opens += 1
        elif token.type == ord(')'):
            opens -= 1

            if opens == 0:
                return i

    return None


def exp_call(tokens, start=0, stop=0):
    found = False

    i = start
    if stop == 0:
        stop = len(tokens)

    while i < stop:
        token = tokens[i]

        if token.type == ExpressionLexer.TAG_FUNCTION:
            arg_stop = exp_call_match(tokens[i + 1:]) + i

            found = True

            if not exp_call(tokens, start=i + 1, stop=arg_stop - 1):
                # reached a point of no more function calls.
                call = tokens[i + 1:arg_stop + 1]

                tokens[i + 1] = Token(str(eval(" ".join([token.lexeme for token in call]))), '(')
                for x in xrange(i + 2, arg_stop + 1):
                    tokens[x] = Token(" ", '(')

                found = False

            i = arg_stop

        i += 1

    return found
"""


if __name__ == '__main__':
    lexer = ExpressionLexer()
    tokens = lexer.parse(
        "let x = cos(1 + sin(2 + cos(3 + 1)) + sin(2)) + (1 + 2) + cos(sin(1))"
    )
    # exp_call(tokens)
    # debug_tokens(tokens)
    print eval(" ".join([token.lexeme for token in tokens[3:]]))
    print eval("cos(1 + sin(2 + cos(3 + 1)) + sin(2)) + (1 + 2) + cos(sin(1))")

"""
let x = a(1 + b(2 + c(3 + 1)) + e(2)) + (1 + 2) + a(b(1))
        |---------------------------|             |-----|
              |-------------|   |--|                |--|
                    |------|      |                   |
"""