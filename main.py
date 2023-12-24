import os
import sys
from Editor import *
from curses import wrapper

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-1000:])
    def get_text(self,beg=0,end=-1):
        return '\n'.join(self.text.split('\n')[beg:end])

def myMain(stdscr):
    editor = Editor() 
    editor.run()

def setShorterEscDelayInOs():
        os.environ.setdefault('ESCDELAY', '25')

mystdout = StdOutWrapper()
sys.stdout = mystdout
sys.stderr = mystdout

try:
    setShorterEscDelayInOs()
    wrapper(myMain)
finally:

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())
    sys.stdout.write("\n")
