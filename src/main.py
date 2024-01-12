import os
import sys
from curses import wrapper

from Editor import *
from JsonPorter import *
from SourcePorter import *

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-1000:])
    def get_text(self,beg=0,end=-1):
        return '\n'.join(self.text.split('\n')[beg:end])

def myMain(stdscr,args):
    i = 0
    help = False
    file = None
    diagram = ""
    format = '\\${diagram:(.*)}'
    while i<len(args):
        arg = args[i]
        i += 1

        if arg=="--help":
            help = True
        elif arg=="--format":
            format = args[i]
            i += 1
        else:
            split = arg.split(':')
            splitLen = len(split)
            if splitLen>=1:
                file = split[0]
            if splitLen==2:
                diagram = split[1]
            elif splitLen>2:
                print("Expect only one diagram name")
                help = True
                break


    if file==None:
        print("Expect file to be specified")
        help = True

    if help:
        print("edit.sh [--format <regular Expression with one group>] <file name>[:<diagram name>]")
        sys.exit(0)

    jsonName = file+".json"
    if os.path.exists(jsonName):
        diagram = JsonPorter.importDiagram(jsonName,diagram)
    else:
        diagram = Diagram(diagram)

    editor = Editor(diagram, lambda : save(file,diagram) ) 
    editor.run()

def save(file,diagram):
    print("saving file '"+file+"' diagram='"+diagram.name+"'")
    JsonPorter.exportDiagram(file+".json",diagram)
    sourcePorter = SourcePorter()
    sourcePorter.writeToFile(file,diagram)
    print("saved")


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
