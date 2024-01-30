import os
import sys
import pathlib
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
    sourceFile = None
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
                sourceFile = split[0]
            if splitLen==2:
                diagram = split[1]
            elif splitLen>2:
                print("Expect only one diagram name")
                help = True
                break


    if sourceFile==None:
        print("Expect file to be specified")
        help = True

    if help:
        print("edit.sh [--format <regular Expression with one group>] <file name>[:<diagram name>]")
        sys.exit(0)

    sourceDiagramDirName = ".sourceDiagrams"

    dotDir = findDirParent(sourceFile,sourceDiagramDirName)
    if dotDir is None:
        gitDir = findDirParent(sourceFile,".git")
        if gitDir is None:
            print("Can find neither .sourceDiagram nor .git dirs.")
            sys.exit(-1)

        dotDir = os.path.join(gitDir.parent,sourceDiagramDirName)
        os.mkdir(dotDir)
        dotDir = pathlib.Path(dotDir)

        print("Found gitDir="+str(gitDir))
        print("create "+sourceDiagramDirName+" at "+str())

    print("dotDir='"+str(dotDir)+"'")
    projRoot = dotDir.parent
    print("projRoot="+str(projRoot))
    relPathOfSource = os.path.relpath(sourceFile,projRoot)
    print("relPathOfSource="+str(relPathOfSource))

    jsonFile = os.path.join(dotDir,relPathOfSource + ".json")

    print("diagram from jsonFile="+jsonFile)
    if os.path.exists(jsonFile):
        diagram = JsonPorter.importDiagram(jsonFile,diagram)
    else:
        diagram = Diagram(diagram)

    editor = Editor(diagram, lambda : save(sourceFile,jsonFile,diagram) ) 
    editor.run()

def findDirParent(file,dirName):
    lastParent = None
    parent = pathlib.Path(file).absolute()
    while True:
        parent = pathlib.Path(parent).parent
        if parent is None or parent==lastParent: # For some reason parent of root is itself (on linux)
            return None
        lastParent = parent

        for file in parent.iterdir():
            #print("testing file="+str(file)+" name="+str(file.name)) 
            if file.is_dir():
                if file.name==dirName:
                    return file

def save(sourceFile,jsonFile,diagram):
    print("saving file '"+sourceFile+"' diagram='"+diagram.name+"'")
    os.makedirs(os.path.dirname(jsonFile),exist_ok=True)
    JsonPorter.exportDiagram(jsonFile,diagram)
    sourcePorter = SourcePorter()
    sourcePorter.writeToFile(sourceFile,diagram)
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
