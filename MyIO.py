

class Section:
    def __init__(self, *, text = ""):
        self.setText(text)

    def setText(self, text):
        if text == "":
            self.text = ""
        else:
            self.text = text.splitlines()[0]

    def render(self, scr, pos): 
        h, w = scr.getmaxyx()
        scr.addnstr(pos, 0, self.text, w)

class IO:
    def __init__(self, pos, scr):
        self.text = ""
        self.h, self.w = scr.getmaxyx()
        self.scr = scr.derwin(1, self.w, self.h - pos, 0)
        self.mainscr = scr
 
    def render(self):
        self.scr.clear()
        self.scr.addstr(0, 0, self.text)
        self.scr.refresh()   

class Inputer(IO):
    esc  = ""
    escD = False
    def render(self):
        IO.render(self)
        self.scr.move(0, self.pos)
    pos = 0
    def move(self, num):
        self.pos = max(min(self.pos + num, len(self.text)), 0)
    def getNext(self):
        ch = self.scr.getkey()
        if ch == "\n":
            t = self.text
            self.text = ""
            self.pos = 0
            return t
        elif ch == "KEY_RESIZE":
            return 1
        elif ch == "KEY_LEFT":
            self.move(-1)
        elif ch == "KEY_RIGHT":
            self.move(1)
        elif ch == "KEY_UP":
            return 2
        elif ch == "KEY_DOWN":
            return 3
        elif ch == "\x1b":
            self.escD = True
        elif ch in ["\x08", "\x7f"]:
            self.text = self.text[:self.pos - 1] + self.text[self.pos:]
            self.move(-1)
        elif len(ch) == 1 and ch.isprintable():
            if self.escD:
                self.esc += ch
            else:
                self.text = self.text[:self.pos] + ch + self.text[self.pos:]
                self.move(1)
        else:
            pass
        if self.escD and len(self.esc) == 2:
            out = None
            if self.esc == "[A":
                out = 2
            elif self.esc == "[B":
                out = 3
            elif self.esc == "[C":
                self.move(1)
            elif self.esc == "[D":
                self.move(-1)
            self.esc = ""
            self.escD = False
            return out
        return None

    def getLine(self):
        out = None
        while out is None:
            out = self.getNext()
            self.render()
        return out

            

class Outputer(IO):
    def setText(self, text):
        if text == "":
            self.text = ""
        else:
            self.text = text.splitlines()[0]
