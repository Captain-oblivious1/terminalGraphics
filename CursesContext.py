import curses

from Context import *

class CursesContext(Context):
    def __init__(self,window):
        super().__init__()
        self.window = window

    def writeString(self,x,y,text,bold=False,reverse=False):
        # TODO: make his adhere to invalidatedRect
        if bold or reverse:
            pair = curses.color_pair(1)
            if bold:
                #pair |= curses.A_BOLD # doesn't work for some reason
                pair |= curses.A_REVERSE
            if reverse:
                pair |= curses.A_REVERSE
            self.window.addstr(y,x,text,pair)
        else:
            self.window.addstr(y,x,text)

    def clearWindow(self):
        self.window.clear()

    def readChar(self,x,y):
        return chr(0xFFFF & self.window.inch(y,x))

    def getMaxXy(self):
        y,x = self.window.getmaxyx()
        return x,y
