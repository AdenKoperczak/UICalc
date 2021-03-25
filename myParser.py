from pyparsing import *
import numpy as np
import copy

class ASTEquation:
    def __init__(self, Type, name, args, expr):
        self.type = Type
        self.name = name
        self.args = args
        self.expr = expr

    def getValue(self, var, *args):
        if self.args is not None and len(self.args) != len(args):
            raise ToFewArgsError(f"{self.name} needs {len(self.args)} arguments, but got {len(args)} arguments.")
        var = copy.deepcopy(var)
        if self.args is not None:
            var.update(dict(zip(self.args, args)))
        return name, self.expr.getValue(args)



class ParsingError(Exception):
    pass
class ToFewArgsError(ParsingError):
    pass

lPar = Suppress("(")
rPar = Suppress(")")

var = Word(alphas)
args = lPar + Group(delimitedList(var)) + rPar
pre = var + Optional(args) + Suppress("=")

expression = Forward()
cArgs = lPar + Group(delimitedList(expression)) + rPar
function = var + cArgs

digits = Word(nums)
sign = Literal("+") ^ Literal("-")
decPlace = "." + digits

numNormal = Combine(digits + Optional(decPlace))
numNoStar = Combine(decPlace)

singleNum = Optional(sign) + numNormal ^ numNoStar

scientificPart = Literal("E") + singleNum
number = Combine(singleNum + Optional(scientificPart))

joinOperator = Literal("+") ^ "-" ^ "*" ^ "/" ^ "^" 

grouper = lPar + Group(expression) + rPar

section = Group(function) ^ grouper ^ number ^ var
expression <<= section + ZeroOrMore(joinOperator + section)

equation = Optional(pre) + Group(expression)

def parse(text):
    base = equation.parseString(text)



if __name__=="__main__":
    while True:
        print(equation.parseString(input("?: ")))
