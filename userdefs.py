from math import *


def poisson(k, l):
    return (l ** k * e ** (-l)) / (factorial(k))
