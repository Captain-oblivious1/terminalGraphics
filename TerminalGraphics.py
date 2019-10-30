#!/bin/python

import curses
import math
from curses.textpad import Textbox, rectangle

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




def main(stdscr):

    screen = curses.initscr()
    curses.curs_set(0)

    screen.clear()
    box = Box(screen,15,26,3,10)

    while True:
        for deg in range(0,360,1):
            box.move(8+int(8*math.sin(math.radians(deg))),40+int(40*math.cos(math.radians(deg))))
            curses.napms(5)

    #box.move(5,11)
    curses.napms(2000)
    #screen.getkey()
    #drawIt()
    ## The `screen` is a window that acts as the master window
    ## that takes up the whole screen. Other windows created
    ## later will get painted on to the `screen` window.
    #screen = curses.initscr()

    #screen.clear()
    ##box = Box(curses,0,0,20,15)
    ##box.draw()
    ##box.refresh()
    ##screen.refresh()

    ## lines, columns, start line, start column
    #my_window = curses.newwin(15, 20, 0, 0)

    ## Long strings will wrap to the next line automatically
    ## to stay within the window
    #my_window.addstr(4, 4, "Hello from 4,4")
    #my_window.addstr(5, 15, "Hello from 5,15 with a long string")

    ### Print the window to the screen
    #my_window.refresh()
    #curses.napms(2000)

    ## Clear the screen, clearing my_window contents that were printed to screen
    ## my_window will retain its contents until my_window.clear() is called.
    #screen.clear()
    #screen.refresh()

    ## Move the window and put it back on screen
    ## If we didn't clear the screen before doing this,
    ## the original window contents would remain on the screen
    ## and we would see the window text twice.
    #my_window.mvwin(10, 10)
    #my_window.refresh()
    #curses.napms(1000)

    ## Clear the window and redraw over the current window space
    ## This does not require clearing the whole screen, because the window
    ## has not moved position.
    #my_window.clear()
    #my_window.refresh()
    #curses.napms(1000)

    curses.endwin()

#    # The `screen` is a window that acts as the master window
#    # that takes up the whole screen. Other windows created
#    # later will get painted on to the `screen` window.
#    screen = curses.initscr()
#    
#    # lines, columns, start line, start column
#    my_window = curses.newwin(15, 20, 0, 0)
#    
#    # Long strings will wrap to the next line automatically
#    # to stay within the window
#    my_window.addstr(4, 4, "Hello from 4,4")
#    my_window.addstr(5, 15, "Hello from 5,15 with a long string")
#    
#    # Print the window to the screen
#    my_window.refresh()
#    curses.napms(2000)
#    
#    # Clear the screen, clearing my_window contents that were printed to screen
#    # my_window will retain its contents until my_window.clear() is called.
#    screen.clear()
#    screen.refresh()
#    
#    # Move the window and put it back on screen
#    # If we didn't clear the screen before doing this,
#    # the original window contents would remain on the screen
#    # and we would see the window text twice.
#    my_window.mvwin(10, 10)
#    my_window.refresh()
#    curses.napms(1000)
#    
#    # Clear the window and redraw over the current window space
#    # This does not require clearing the whole screen, because the window
#    # has not moved position.
#    my_window.clear()
#    my_window.refresh()
#    curses.napms(1000)
#    
#    curses.endwin()
##def main(stdscr):
##    stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
##
##    editwin = curses.newwin(5,30, 2,1)
##    rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
##    stdscr.refresh()
##
##    box = Textbox(editwin)
##
##    # Let the user edit until Ctrl-G is struck.
##    box.edit()
##
##    # Get resulting contents
##    message = box.gather()
#
##import curses

from curses import wrapper
#
#def main(stdscr):
#    # Clear screen
#    stdscr.clear()
#
#    stdscr = curses.initscr()
#
#    stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
#    curses.noecho()
#    curses.cbreak()
#
#    #begin_x = 20; begin_y = 7
#    #height = 5; width = 40
#    #win = curses.newwin(height, width, begin_y, begin_x)
#
#    stdscr.refresh()
#    stdscr.getkey()
#
wrapper(main)

