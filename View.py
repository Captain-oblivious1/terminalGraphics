#!/bin/python

import os
import sys
import curses
from Model import *
from Components import *
from ConnectorComponent import *
from PathComponent import *
from OpenPath import *
from ClosedPath import *
from curses import wrapper

# The following is so that I can more easily do more advanced drawing.
#
# So like this:    │        Not this:    │
#               ┌──┴──┐               ┌─────┐
#             ──┤ box ├──           ──│ box │──
#               └──┬──┘               └─────┘
#                  │                     │
#

# 4D array for all possible box chars
# boxArray [left][right][top][bottom]
# None:      " "   " "   " "   " "
# Thin:      "╴"   "╶"   "╵"   "╷"
# Thick:     "╸"   "╺"   "╹"   "╻"
boxArray = [  
  [ [ [ " ", "╷", "╻"], [ "╵", "│", "╽"], [ "╹", "╿", "┃"] ],
    [ [ "╶", "┌", "┎"], [ "└", "├", "┟"], [ "┖", "┞", "┠"] ],
    [ [ "╺", "┍", "┏"], [ "┕", "┝", "┢"], [ "┗", "┡", "┣"] ] ],
  [ [ [ "╴", "┐", "┒"], [ "┘", "┤", "┧"], [ "┚", "┦", "┨"] ],
    [ [ "─", "┬", "┰"], [ "┴", "┼", "╁"], [ "┸", "╀", "╂"] ],
    [ [ "╼", "┮", "┲"], [ "┶", "┾", "╆"], [ "┺", "╄", "╊"] ] ],
  [ [ [ "╸", "┑", "┓"], [ "┙", "┥", "┧"], [ "┛", "┩", "┫"] ],
    [ [ "╾", "┭", "┱"], [ "┵", "┽", "╅"], [ "┹", "╃", "╉"] ],
    [ [ "━", "┯", "┳"], [ "┷", "┿", "╈"], [ "┻", "╇", "╋"] ] ] ]

# I made up a scheme that allows me to create box characters by 
# or-ing and and-ing other characters.  I assign each character a
# value based an integer that has "pixels" activated.  The follow
# indicates what bits represent what pixel.
#    ┌──┰──┬──┐      All box characters can be created by bitwise
#    │21┃20│19│      or-ing any of the following:
# ┌──┼──╂──┼──┼──┐   " " = 0x0
# │18│17┃16│15│14│   "╴" = 0x1C00
# ├──╁──╀──┼──┼──┤   "╸" = 0x39CE0
# │13┃12│11│10│ 9│   "╶" = 0x700
# ┟──╀──┼──┼──╁──┤   "╺" = 0xE738
# ┃ 8│ 7│ 6│ 5┃ 4│   "╵" = 0x88400
# ┖──┼──┼──┼──╂──┘   "╹" = 0x1DCE00
#    │ 3│ 2│ 1┃      "╷" = 0x422
#    └──┴──┴──┚      "╻" = 0xE77
# (I blew off the double line versions because there are no
# Unicode characters that mix and match them.  For example
# I can simulate or-ing "│" with "━" by using the "┿" char.
# But there is no equivalent for the or of "║" and "━". Only
# "║" and "─" (which is "╫").  I think thicker lines is more
# useful than double lines.  Double lines look too DOSy.

charToHexMap = {}
hexToCharMap = {}

def intializeMaps():
    leftArray =   [ 0x0, 0x1C00,  0x39CE0  ]
    rightArray =  [ 0x0, 0x700,   0xE738   ]
    topArray =    [ 0x0, 0x88400, 0x1DCE00 ]
    bottomArray = [ 0x0, 0x422,   0xE77    ]

    for left in range(3):
        for right in range(3):
            for top in range(3):
                for bottom in range(3):
                    value = leftArray[left] | rightArray[right] | topArray[top] | bottomArray[bottom]
                    char = boxArray[left][right][top][bottom]
                    charToHexMap[char] = value
                    hexToCharMap[value] = char

    # insert half blocks into charToHexMap for masking stuff (don't put in hextToCharMap)
    charToHexMap["▀"]=0x1FFF00
    charToHexMap["▄"]=0x1FFF
    charToHexMap["▌"]=0x1B9CE6
    charToHexMap["▐"]=0xCE33B

    charToHexMap["▘"]=0x1B9C00
    charToHexMap["▝"]=0xCE700
    charToHexMap["▖"]=0x1CE6
    charToHexMap["▗"]=0x73B

    charToHexMap["▙"]=0x1B9FFF
    charToHexMap["▛"]=0x1FFFE6
    charToHexMap["▜"]=0x1FFF3B
    charToHexMap["▟"]=0xCFFFF

intializeMaps()

def charToHex(char):
    if char in charToHexMap:
        return charToHexMap[char]
    else:
        return 0

def hexToChar(hex):
    if hex in hexToCharMap:
        return hexToCharMap[hex]
    else: # find closest match
        # If this is slow, do more fancy bit-wise math
        minDiff = 64
        minChar = None
        for key,value in hexToCharMap.items():
            count = bin(hex ^ key).count("1")
            if count<minDiff:
                minDiff = count
                minChar = value
        return minChar

def orChars(char1,char2):
    return hexToChar( charToHex(char1) | charToHex(char2) )

def andChars(char1,char2):
    return hexToChar( charToHex(char1) & charToHex(char2) )


class Context:
    def __init__(self,window):
        self.window = window
        self.invalidatedRect = Rect()

    def addString(self,x,y,text,bold=False,reverse=False):
        if bold or reverse:
            pair = curses.color_pair(1)
            if bold:
                pair |= curses.A_BOLD
            if reverse:
                pair |= curses.A_REVERSE
            self.window.addstr(y,x,text,pair)
        else:
            self.window.addstr(y,x,text)

    def readChar(self,x,y):
        return chr(0xFFFF & self.window.inch(y,x))

    def clearRect(self,rect=None):
        if rect == None:
            self.window.clear()
        elif not rect.isNullRect() :
            for i in range(0,rect.width()):
                for j in range(0,rect.height()):
                    self.addString(rect.x()+i,rect.y()+j," ")

    def orChar(self,x,y,char,isBold=False):
        charOrd = ord(char)
        if (charOrd>=0x2500 and charOrd<=0x254b) or (charOrd>=0x2574 and charOrd<=0x257f):
            #if is a box char
            existing = self.readChar(x,y)
            writeMe = orChars(existing,char)
        else:
            writeMe = char
        self.addString(x,y,writeMe,isBold)

    def andChar(self,x,y,char,isBold=False):
        if char!="█":
            existing = self.readChar(x,y)
            writeMe = andChars(existing,char)
            self.addString(x,y,writeMe,isBold)

    def drawVerticalLine(self,x,fro=0,to=None,isBold=False):
        if to==None:
            to,_ = self.window.getmaxyx()
            to -= 1
        maxY = max(fro,to)
        minY = min(fro,to)
        for i in range(minY,maxY+1):
            self.orChar(x,i,"│",isBold)

    def drawHorizontalLine(self,y,fro=0,to=None,isBold=False):
        if to==None:
            _,to = self.window.getmaxyx()
            to -= 1
        maxX = max(fro,to)
        minX = min(fro,to)
        for i in range(minX,maxX+1):
            self.orChar(i,y,"─",isBold)

    def invalidateComponent(self,component):
        self.invalidateRect(component.getRect())
        if "invalidateMe" in dir(component):
            component.invalidateMe(self)

    def invalidateRect(self,rect):
        self.invalidatedRect.unionWith(rect)

    def validateAll(self):
        self.invalidatedRect = Rect()

    def getInvalidatedRect(self):
        return self.invalidatedRect

    def allInvalidatedComponents(self):
        return self.invalidatedComponents

class State:
    def __init__(self):
        pass

    def mouseMoved(self, x, y):
        pass
        #print("Mouse moved to x="+str(x)+" y="+str(y))

    def mouseClicked(self, x, y):
        pass
        #print("Mouse clicked to x="+str(x)+" y="+str(y))

    def mousePressed(self, x, y):
        pass
        #print("Mouse pressed to x="+str(x)+" y="+str(y))

    def mouseReleased(self, x, y):
        pass
        #print("Mouse released to x="+str(x)+" y="+str(y))

    def keyPressed(self,char):
        pass
        #print("Key pressed '"+str(char)+"'")

class IdleState(State):
    def __init__(self,editor,context,diagramComponent):
        self.editor = editor
        self.context = context
        self.diagramComponent = diagramComponent
        self.startDragPoint = None
        self.movingComponents = False

    def mousePressed(self, x, y):
        # Curses does not support testing of shift, ctrl, alt, etc.  So I can't 
        # pretend I'm powerpoint here

        self.startDragPoint = Point(x,y)

        selectedSet = self.diagramComponent.allSelected()

        clickedOn = self.diagramComponent.componentAt(self.startDragPoint)

        if clickedOn==None or not clickedOn in selectedSet:
            for component in selectedSet:
                component.setSelected(False)
                self.context.invalidateComponent(component)

        if clickedOn!=None:
            self.movingComponents = True
            clickedOn.setSelected(True)
            #print("Invalidating clicked on")
            self.context.invalidateComponent(clickedOn)

    def mouseReleased(self, x, y):
        self.startDragPoint = None
        self.movingComponents = False

    def mouseMoved(self, x, y):
        if self.startDragPoint!=None:
            if self.movingComponents:
                self.editor.setState(MovingState(self.editor,self.context,self.diagramComponent,self.startDragPoint))
            else:
                self.editor.setState(LassoState(self.editor,self.context,self.diagramComponent,self.startDragPoint))

class LassoState(State):
    def __init__(self,editor,context,diagramComponent,startDragPoint):
        self.editor = editor
        self.context = context
        self.diagramComponent = diagramComponent
        self.startDragPoint = startDragPoint
        self.oldRect = None

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        if self.oldRect!=None:
            for component in self.diagramComponent.children():
                if self.oldRect.isInsideRect(component.getRect()):
                    component.setSelected(True)
                else:
                    component.setSelected(False)

            self.context.invalidateRect( self.oldRect )
            self.diagramComponent.setSelectionRect(None)

        self.editor.setState(IdleState(self.editor,self.context,self.diagramComponent))

    def mouseMoved(self, x, y):
        startX=self.startDragPoint.x
        startY=self.startDragPoint.y

        topLeft = Point( min(startX,x), min(startY,y) )
        bottomRight = Point( max(startX,x), max(startY,y) )

        rect = Rect.makeRectFromPoints(topLeft,bottomRight)
        self.diagramComponent.setSelectionRect(rect)
        self.context.invalidateRect(rect)
        if self.oldRect!=None:
            self.context.invalidateRect(self.oldRect)
        self.oldRect = rect

class MovingState(State):
    def __init__(self,editor,context,diagramComponent,startDragPoint):
        self.editor = editor
        self.context = context
        self.diagramComponent = diagramComponent
        self.lastPoint = startDragPoint

        self.selectedComponents = diagramComponent.allSelected()

        selectedElements = set()
        for component in self.selectedComponents:
            selectedElements.add(component.element)

        self.affectedConnectors = set()
        for component in self.diagramComponent.children():
            if issubclass(type(component),ConnectorComponent):
                connectorElement = component.element
                if connectorElement.fromConnection.element in selectedElements or connectorElement.toConnection.element in selectedElements:
                    self.affectedConnectors.add(component)

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        self.editor.setState(IdleState(self.editor,self.context,self.diagramComponent))

    def mouseMoved(self, x, y):
        newPoint = Point(x,y)
        offset = newPoint - self.lastPoint
        if offset!=Point(0,0):

            # Invalidate the location where the connectors were (to erase them if necessary)
            for component in self.affectedConnectors:
                self.context.invalidateComponent(component)

            for component in self.selectedComponents:
                self.context.invalidateComponent(component)
                component.move(offset,self.context)
                self.context.invalidateComponent(component)

            self.lastPoint = newPoint

            # Invalidate the new location where the connectors are now
            for component in self.affectedConnectors:
                self.context.invalidateComponent(component)

def createTestDiagram():
    diagramElement = Diagram()
    #textBoxElement1 = testTextBox()
    ##textBoxElement1.x = 0
    ##textBoxElement1.y = 20
    #textBoxElement1.x = 20
    #textBoxElement1.y = 10
    #diagramElement.elements.append(textBoxElement1)

    #textBoxElement2 = testTextBox()
    #textBoxElement2.x = 60
    #textBoxElement2.y = 20
    #diagramElement.elements.append(textBoxElement2)


    #fromConnectionPoint1 = ConnectionPoint()
    #fromConnectionPoint1.element = textBoxElement1
    #fromConnectionPoint1.side = Direction.RIGHT
    #fromConnectionPoint1.where = 0.5
    #fromConnectionPoint1.end = Arrow.NONE

    #toConnectionPoint1 = ConnectionPoint()
    #toConnectionPoint1.element = textBoxElement2
    #toConnectionPoint1.side = Direction.LEFT
    #toConnectionPoint1.where = 0.25
    #toConnectionPoint1.end = Arrow.TRIANGLE

    #connectorElement1 = ConnectorElement()
    #connectorElement1.fromConnection = fromConnectionPoint1
    #connectorElement1.toConnection = toConnectionPoint1
    #connectorElement1.controlPoints.append(45)
    #diagramElement.elements.append(connectorElement1)

    #fromConnectionPoint2 = ConnectionPoint()
    #fromConnectionPoint2.element = textBoxElement1
    #fromConnectionPoint2.side = Direction.DOWN
    #fromConnectionPoint2.where = 1.0
    #fromConnectionPoint2.end = Arrow.LINES

    #toConnectionPoint2 = ConnectionPoint()
    #toConnectionPoint2.element = textBoxElement2
    #toConnectionPoint2.side = Direction.UP
    #toConnectionPoint2.where = 0.5
    #toConnectionPoint2.end = Arrow.NONE

    #connectorElement2 = ConnectorElement()
    #connectorElement2.fromConnection = fromConnectionPoint2
    #connectorElement2.toConnection = toConnectionPoint2
    #connectorElement2.controlPoints.append(19)
    #connectorElement2.controlPoints.append(51)
    #connectorElement2.controlPoints.append(15)
    #diagramElement.elements.append(connectorElement2)

    pathElement = PathElement()
    pathElement.pathType = PathType.CLOSED #OPEN

    #pathElement.startOrientation = Orientation.HORIZONTAL
    #pathElement.turns = [80,5,85,30,75,24]
    #pathElement.turns = [80,5,85,30,75,24,80,5]
    pathElement.startOrientation = Orientation.VERTICAL
    pathElement.turns = [5,23,12,30,20,2]
    pathElement.corners = Corners.ROUNDED
    diagramElement.elements.append(pathElement)

    return diagramElement

def createDiagramComponent(diagramElement):
    diagramComponent = DiagramComponent(diagramElement)

    for element in diagramElement.elements:
        if type(element) is TextBoxElement:
            component = TextBoxComponent(element)
        elif type(element) is ConnectorElement:
            component = ConnectorComponent(element)
        elif type(element) is PathElement:
            if element.pathType == PathType.CLOSED:
                pathRenderer = ClosedPath(element.startOrientation)
            else:
                pathRenderer = OpenPath(element.startOrientation)
            component = PathComponent(element,pathRenderer)

        diagramComponent.components.append(component)

    return diagramComponent


class Editor:
    def __init__(self):
        self.state = State()

    def setState(self,state):
        self.state = state

    def run(self):
        screen = curses.initscr()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        screen.clear()
        #screen.addstr(0,0,"Hello",curses.color_pair(1)|curses.A_BOLD)

        diagram = createTestDiagram()
        print("============")
        diagramComponent = createDiagramComponent(diagram)

        context = Context(screen)
        self.state = IdleState(self,context,diagramComponent)

        diagramComponent.invalidateAll(context)
        diagramComponent.draw(context)
        screen.refresh()
        context.validateAll()

        curses.mouseinterval(0)

        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        while(True):
            event = screen.getch()
            #print("event='"+str(curses.keyname(event))+"'")
            #ch = 'N'
            if event == 27:
                screen.nodelay(True)
                nextKey = screen.getch()
                screen.nodelay(False)
                if nextKey==-1:
                    break;
            #elif event == ord('q'):
            #    break
            elif event == curses.KEY_MOUSE:
                #ch = 'Y'
                _ , mx, my, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON1_CLICKED != 0:
                    self.state.mouseClicked(mx,my)
                elif bstate & curses.BUTTON1_PRESSED != 0:
                    self.state.mousePressed(mx,my)
                elif bstate & curses.BUTTON1_RELEASED != 0:
                    self.state.mouseReleased(mx,my)
                else:
                    self.state.mouseMoved(mx,my)
            else:
                self.state.keyPressed(event)

            diagramComponent.draw(context)
            context.validateAll()
            screen.refresh()

        curses.endwin()

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])
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
