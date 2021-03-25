import re
import yaml
import os
from settings import *
import copy 

here = os.path.abspath(os.path.dirname(__file__))
def joinPath(*path):
    return os.path.join(here, *path)

class MyEnum(object):
    def __init__(self, dic):
        self.dic = dic
    def __getattr__(self, key):
        if key in ["__getattr__", "__init__", "dic"]:
            return object.__getattribute__(self, key)
        else:
            try:
                return self.dic[key]
            except KeyError:
                raise AttributeError(f"Key {key} not in Enum") 

override = [
    "print",
    "open",
    "input"
]

class EquationBase:
    CONSTANTS = None
    def __init__(self, eqVars, *, equ=""):
        self.setEqu(equ)
        self.vars = eqVars
        self.getGlobals()
        self.addConstants()

    def getGlobals(self):
        self.glob = {}

    def overRidebuiltins(self):
        for item in override:
            self.glob[item] = None

    def addConstants(self):
        if self.CONSTANTS is None:
            filename = joinPath("constants.yaml")
            if os.path.exists(filename):
                with open(filename) as file:
                     type(self).CONSTANTS = MyEnum(yaml.load(file, Loader=yaml.FullLoader))
        self.glob["cons"] = self.CONSTANTS

    def setEqu(self, equ):
        self.equ = equ.split(";")[0]
    def getEqu(self):
        return self.equ

    def calculate(self):
        glob = copy.copy(self.glob)
        glob.update(self.vars)
        if re.match("[^=]*=[^=]", self.equ):
            exec(self.equ, glob, self.vars)
            key = self.equ.partition("=")[0]
            value = eval(key, {}, self.vars)
            return value
        else:
            return eval(self.equ, glob)

    def render(self):
        value = self.calculate()
        if isinstance(value, (int, float)):
            if abs(value) < LOWER_SCI or abs(value) > HIGHER_SCI:
                value = format(value, SCI_FORM_PRS)
                frac, S, exp = value.partition(SCI_FORM)
                frac = frac.rstrip("0").rstrip(".")
                value = frac + S + exp
            else:
                value = format(value, FIX_FORM_PRS).rstrip("0").rstrip(".")
        elif callable(value):
            value = self.equ.partition("=")[0]
        else:
            value = str(value)
        return self.equ, value

class EquationMath(EquationBase):
    def getGlobals(self):
        import math
        self.glob = math.__dict__

class EquationNumPy(EquationBase):
    def integ(self, lower, upper, equ, *, steps=1E6):
        x = self.glob["linspace"](lower, upper, int(steps))
        equ.__globals__.update(self.vars)
        y = equ(x)
        return self.glob["trapz"](y, x)
    def getGlobals(self):
        import numpy
        self.glob = numpy.__dict__
        self.glob["integ"] = self.integ

Equation = EquationNumPy

