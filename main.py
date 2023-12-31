import os
import sys
from curses import wrapper

from Editor import *
from FileParser import *

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-1000:])
    def get_text(self,beg=0,end=-1):
        return '\n'.join(self.text.split('\n')[beg:end])

def myMain(stdscr,args):
    i = 0
    file = None
    diagram = None
    format = '\\${diagram:(.*)}'
    while i<len(args):
        arg = args[i]
        i += 1

        if arg=="--file":
            file = args[i]
            i += 1

        if arg=="--diagram":
            diagram = args[i]
            i += 1

        if arg=="--format":
            format = args[i]
            i += 1

    fileParser = FileParser(format)
    diagram = fileParser.loadFromFile(file,diagram,format)

    editor = Editor(diagram) 
    editor.run()

def setShorterEscDelayInOs():
        os.environ.setdefault('ESCDELAY', '25')

mystdout = StdOutWrapper()
sys.stdout = mystdout
sys.stderr = mystdout

try:
    setShorterEscDelayInOs()
    wrapper(myMain,sys.argv[1:])
finally:

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())
    sys.stdout.write("\n")
