import os
import sys
from curses import wrapper

from Editor import *
from JsonPorter import *
from SourcePorter import *
from MemoryContext import *

def createTestDiagram():
    diagramElement = Diagram()
    diagramElement.name = "The diagram"

    #diagramElement.elements.append(RectElement( Rect(5,6,10,7) ))
    #diagramElement.elements.append(RectElement( Rect(8,13,16,8) ))

    pathElement1 = PathElement()
    #pathElement1.pathType = PathType.CLOSED
    pathElement1.pathType = PathType.OPEN
    pathElement1.fill = Fill.OPAQUE
    pathElement1.startOrientation = Orientation.VERTICAL
    #pathElement1.turns = [5,23,12,30,20,2]
    pathElement1.turns = [15,40,20,50,30,60]
    #pathElement1.turns = [0,0,10,20]
    #pathElement1.corners = Corners.ROUND
    pathElement1.corners = Corners.SQUARE
    pathElement1.startArrow = Arrow.LINES
    pathElement1.endArrow = Arrow.TRIANGLE
    diagramElement.elements.append(pathElement1)

    #pathElement2 = PathElement()
    #pathElement2.pathType = PathType.OPEN
    ##pathElement2.fill = Fill.OPAQUE
    #pathElement2.startOrientation = Orientation.VERTICAL #HORIZONTAL
    #pathElement2.turns = [15,40,20,50,30,60]
    #pathElement2.corners = Corners.SQUARE
    #pathElement2.startArrow = Arrow.LINES
    #pathElement2.endArrow = Arrow.TRIANGLE
    #diagramElement.elements.append(pathElement2)

    pathElement3 = PathElement()
    pathElement3.pathType = PathType.CLOSED
    pathElement3.fill = Fill.OPAQUE
    pathElement3.startOrientation = Orientation.VERTICAL
    pathElement3.turns = [5,5,15,25,30,30]
    pathElement3.corners = Corners.ROUND
    diagramElement.elements.append(pathElement3)

    textElement = TextElement()
    textElement.text = "Duane was here.\nYet\nagain."
    textElement.location = Point(20,10)
    textElement.justification = Justification.CENTER
    diagramElement.elements.append(textElement)

    return diagramElement


class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-10000:])
    def get_text(self,beg=0,end=-1):
        return '\n'.join(self.text.split('\n')[beg:end])

def myMain(stdscr,args):

    #diagram = createTestDiagram()
    #JsonPorter.exportDiagram("testJson.json",diagram)
    diagram = JsonPorter.importDiagram("testJson.json","The diagram")
    #import pprint
    #pprint.pprint(JsonPorter._convertToDictionary(diagram))

    diagramComponent = DiagramComponent(None,diagram)
    memContext = MemoryContext(80,50)
    memContext.invalidateRect()
    diagramComponent.draw(memContext)
    memContext.print('// ')

    #sourcePorter = SourcePorter()
    #sourcePorter.writeToFile('TestDiagram.cpp',diagram,'One')

    #editor = Editor(diagram) 
    #editor.run()

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
