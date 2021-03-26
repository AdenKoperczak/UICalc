import curses
import os
import time
from MyIO import *
from Commands import Commands, Equation
import re

INDEXED = ["change", "del", "insert"]

class CalcError(Exception):
    pass

def main(scr):
    Equation({})
    commands = Commands()

    inputer = Inputer(2, scr)
    outputer = Outputer(1, scr)
    sections = [] 
    equations = [] 
    history = []
    historyPos = 0
    var = {}

    controls = {
        "inputer": inputer,
        "outputer": outputer,
        "sections": sections,
        "equations": equations,
        "var": var,
        "run": None
    }
    def getLast(i = -1):
        if len(history) < abs(i) or i > -1:
            return ""
        else:
            return history[i]

    while True:
        inp = inputer.getLine()
        if isinstance(inp, int):
            if inp == 2:
                historyPos = max(historyPos - 1, -len(history))
                inputer.text = getLast(historyPos)
                inputer.move(len(inputer.text))
            elif inp == 3:
                historyPos = min(historyPos + 1, 0)
                inputer.text = getLast(historyPos)
                inputer.move(len(inputer.text))
        elif isinstance(inp, str):
            historyPos = 0
            inp = inp.replace("!!", getLast())
            history.append(inp)
            inp = inp.replace("!\!", "!!")
            com, _, rest = inp.partition(" ")
            outputer.setText("")
            if com not in commands:
                outputer.setText(f"Unknown command {com}")
            else:
                try:
                    run = True
                    command = commands[com]
                    args = [rest]
                    if "index" in command.args:
                        index, _, rest = rest.partition(" ")
                        try:
                            index = int(index)
                        except ValueError:
                            raise CalcError("Index (first argument) must be an integer.")
                        length = len(equations)
                        args.insert(0, index)
                        args[-1] = rest
                        if index >= length or index < -length:
                            if length > 0:
                                raise CalcError(f"Index must be between {-length} and {length - 1} inclusive.")
                            else:
                                raise CalcError("There are no equations. Try using \"add\" to add one.")

                    resp = command.func(*args, controls = controls)
                    if resp == "EXIT":
                        return
                except CalcError as e:
                    outputer.setText(str(e))
            for item in list(var):
                del var[item]
            scr.clear()
            for i, (equation, section) in enumerate(zip(equations, sections)):
                try:
                    equ, res = equation.render()
                except Exception as e:
                    if outputer.text == "":
                        outputer.setText(f"Error in equation {i}: {e}")
                    equ = equation.getEqu()
                    section.setText(f"{i}: {equ}")
                else:
                    section.setText(f"{i}: {equ} = {res}")
                section.render(scr, i)
            if controls["run"] is not None and outputer.text == "":
                equation = Equation(var, equ = controls["run"])
                try:
                    equ, res = equation.render()
                except Exception as e:
                    equ = equation.getEqu()
                    outputer.setText(f"Error running {equ}: {e}")
                else:
                    outputer.setText(f"{equ} = {res}")
                controls["run"] = None
            scr.refresh()
        outputer.render()
        inputer.render()
curses.wrapper(main)
