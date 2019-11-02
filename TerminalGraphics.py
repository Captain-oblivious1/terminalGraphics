#!/bin/python

import curses
import math
import sys
from curses.textpad import Textbox, rectangle
from curses import wrapper

# §§§§§  

#                                         ┌─┐
#                                         ║"│
#                                         └┬┘
#           ┌─────────────┐               ┌┼┐
#           │Bob on       │                │             ┌────┐
#           │several lines│               ┌┴┐            │Last│
#           └──────┬──────┘              Alice           └─┬──┘
#                  │        hello          │               │
#                  │──────────────────────⇥│               │
#                  │                       │               │
#                  │                       │ ╔═════════════╧══╗
#                  │                       │ ║this is a note  ║
#                  │                       │ ╚═════════════╤══╝
#                  │Is it ok               │ ╔═════════════╧════╗
#                  │with a message that is │ ║This other note   ║
#                  │on several lines?      │ ║should work       ║
#                  │<──────────────────────│ ║on several lines  ║
#                  │                       │ ╚═════════════╤════╝
#                  │                       │               │
#                  │              ╔════════╧═════════════╗ │
#══════════════════╪══════════════╣ This is a separation ╠═╪════════════════════════════════════
#                  │              ╚════════╤═════════════╝ │
#                  │                       │               │
#                  │            Yes it works!              │
#                  │──────────────────────────────────────>│
#                  │                       │               │
#                  │                       ╔══════════════╗│────┐
#                  │                       ║this is       ║│    │ working in progress
#                  │                       ║another note  ║│<───┘
#                  │                       ╚══════════════╝│
#                  │                       │               │─ ─ ┐
#                  │                       │               │    | working in progress
#                  │                       │               │< ─ ┘
#                  │                       │               │
#                  │                 done  │               │
#                  │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
#                  │                       │               │
# ╔══════╤═════════╪═══════════════════════╪═══════════════╪════════════╗
# ║ OPT  │  dummy comment                  │               │            ║
# ╟──────┘         │                       │               │            ║
# ║                │                       │               │            ║
# ║                │               Error   │               │            ║
# ║                │               On      │               │            ║
# ║                │               Several │               │            ║
# ║                │               Line    │               │            ║
# ║                │──────────────────────────────────────>│            ║
# ║                │                       │               │            ║
# ║                │                 None  │               │            ║
# ║                │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │            ║
# ╠════════════════╪═══════════════════════╪═══════════════╪════════════╣
# ║                │                       │               │            ║
# ║                │                 None  │               │            ║
# ║                │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │            ║
# ║                │                       │               │            ║
# ║                │                 None  │               │            ║
# ║                │<──────────────────────────────────────│            ║
# ╠════════════════╪═══════════════════════╪═══════════════╪════════════╣
# ║ [other]        │                       │               │            ║
# ║                │                 None  │               │            ║
# ║                │<──────────────────────────────────────│            ║
# ║                │                       │               │            ║
# ║                │                    ╔══╧═══════════════╧══╗         ║
# ║                │                    ║This is a long note  ║         ║
# ║                │                    ║over Alice and Last  ║         ║
# ║                │                    ╚══╤═══════════════╤══╝         ║
# ║                │                 None  │               │            ║
# ║                │<──────────────────────────────────────│            ║
# ║                │                       │               │            ║
# ║                │                 None  │               │            ║
# ║                │<──────────────────────────────────────│            ║
# ╚════════════════╪═══════════════════════╪═══════════════╪════════════╝
#           ┌──────┴──────┐              Alice           ┌─┴──┐
#           │Bob on       │               ┌─┐            │Last│
#           │several lines│               ║"│            └────┘
#           └─────────────┘               └┬┘
#                                         ┌┼┐
#                                          │
#                                         ┌┴┐              [

class Shape:
    pass

    def draw():
        pass


class Box:
    def __init__(self,parent,h,w,y,x):

        self.parent = parent
        # lines, columns, start line, start column
        self.window = curses.newwin(h, w, y, x);
        self.addBorder()
        #self.window.border("│","│","─","─","┌","┐","└","┘")
        self.innerWindow = self.window.subwin(h-2, w-2, y+1, x+1 );
        #self.innerWindow.border('l','r','t','b','q','p','z','m');
        # Long strings will wrap to the next line automatically
        # to stay within the window
        self.innerWindow.addstr(4, 4, "Hello from 4,4")
        self.innerWindow.addstr(5, 15, "Hello from 5,15 with a long string")

        ## Print the window to the screen
        self.window.refresh()

    def addBorder(self):
        try:
            height,width = self.window.getmaxyx()
            height -= 1
            width -= 1

            for x in range(1,width):
                self.window.addstr(0,x,"─")
                self.window.addstr(height,x,"─")

            for y in range(1,height):
                self.window.addstr(y,0,"│")
                self.window.addstr(y,width,"│")

            self.window.addstr(0,0,"┌")
            self.window.addstr(0,width,"┐")
            self.window.addstr(height,0,"└")
            self.window.addstr(height,width,"┘")

        except curses.error:
            pass  #stupid bug in curses after writing to the last character of a window


    def move(self,y,x):
        print("x="+str(x)+" y="+str(y))
        self.parent.clear()
        self.window.mvwin(y,x)
        self.parent.refresh()
        self.window.refresh()


class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])
    def get_text(self,beg=0,end=-1):
        return '\n'.join(self.text.split('\n')[beg:end])

def main(stdscr):
    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    try:
        screen = curses.initscr()
        curses.curs_set(0)

        screen.clear()
        box = Box(screen,15,26,3,10)

        for x in range(0,30):
            for y in range(0,20):
                print(str(screen.inch(y,x))+" ")
            print()

        #while True:
        #    for deg in range(0,360,1):
        #        box.move(8+int(8*math.sin(math.radians(deg))),40+int(40*math.cos(math.radians(deg))))
        #        curses.napms(5)

        print("!!!!!!!!!!!!!")
        curses.napms(2000)

        curses.endwin()
    finally:

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.write(mystdout.get_text())
        sys.stdout.write("\n")

wrapper(main)

