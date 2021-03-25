import inspect
from MyIO import Section
from equation import Equation

class Command:
    def __init__(self, args, names):
        self.args = args
        self.names = names
        self.func = None
    
    def __call__(self, func):
        self.func = func
        return self

class Commands:
    def __init__(self):
        self.funcs = {}
        for other, func in inspect.getmembers(self, lambda item: isinstance(item, Command)):
            for name in func.names:
                self.funcs[name] = func

    def __getitem__(self, key):
        return self.funcs[key]

    def __contains__(self, key):
        return key in self.funcs
    
    @Command([], ["exit", "quit"])
    def exit(rest, *, controls):
        return "EXIT"

    @Command([], ["add"])
    def add(rest, *, controls):
        controls["equations"].append(Equation(controls["var"], equ = rest))
        controls["sections"].append(Section())

    @Command([], ["run"])
    def run(rest, *, controls):
        controls["run"] = rest

    @Command([], ["constants"])
    def constants(rest, *, controls):
        controls["outputer"].setText(", ".join(Equation.CONSTANTS.dic.keys()))

    @Command([], ["clear"])
    def clear(rest, *, controls):
        for i in range(len(controls["equations"])):
            controls["equations"].pop()
            controls["sections"].pop()

    @Command(["index"], ["change", "set"])
    def change(index, rest, *, controls):
        if len(rest) > 0:
            controls["equations"][index].setEqu(rest)
        else:
            text = f"change {index} " + controls["equations"][index].getEqu()
            controls["inputer"].text = text
            controls["inputer"].move(len(text))


    @Command(["index"], ["del", "rm"])
    def rm(index, rest, *, controls):
        del controls["equations"][index]
        del controls["sections"][index]
        
    @Command(["index"], ["insert"])
    def insert(index, rest, *, controls):
        controls["equations"].insert(index, Equation(controls["var"], equ = rest))
        controls["sections"].insert(index, Section())

if __name__=="__main__":
    commands = Commands()
    print(commands["exit"].func("", controls = ""))
