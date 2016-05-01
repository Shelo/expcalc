# Expression Calculator

This software is a calculator based on expressions, with full field
for expandability, the user can define its out functions in python
that can use inside the calculator using expressions.

## Concepts

### Expression

An expression in this calculator is a pair of a key and value, the key
is the expression name, and the value tells on how to calculate the
numerical value of the expression.

Everything here is an expression, since the calculator actually does
no calculation until the user wants an answer explicitly.

This allows you to define everything in whatever order you wish, and
actually be sure that the answers will be up to date with the last data
entered, giving the flexibility of just putting out formulas and then
worry about the real numerical values.

### Command

A command tells the calculator what to do with the following data, it
is a simplification for the parser and actually makes the code more
maintainable.

## Expandability

The user can expand the library of functions, the first time the user
executes the calculator, the `.expcalc.py` file will be created at
the user home. Inside this file add functions at will, like so:

```
from math import *


def poisson(k, l):
    return (l ** k * e ** (-l)) / (factorial(k))
```

## Usage

## Defining expressions

An expression can be defined with the following syntax:

```
let <exp_name> = <exp_value>
```

Example

```
let x = a + b
let a = 2
let b = 5
```

## Calculating expression values

As said before, expression are calculated on-demand, as so:

```
out x
```

Example

```
let x = a + b
let a = 2
let b = pi
out x
```

Output

```
[x] 5.14159
```

Also, it is possible to calculate values without a previously defined 
expression:

```
let a = cos(2)
let b = 5
a + b
```

Output
```
[a + b] 4.58385
```

## Utility commands

### Exp

Returns the expression of a given name.

```
let x = a + b
exp x
```

Output

```
[x] a + b 
```
