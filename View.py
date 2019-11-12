#!/bin/python

import sys
import curses
from Model import *
from Components import *
from curses import wrapper
#import keyboard


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
        #inch=self.window.inch(y,x)
        #print("inch="+hex(inch))
        return chr(0xFFFF & self.window.inch(y,x))

    def clearRect(self,rect=None):
        if rect == None:
            self.window.clear()
        elif not rect.isNullRect() :
            #self.clear(rect.x(),rect.y(),rect.width(),rect.height())
            for i in range(0,rect.width()):
                for j in range(0,rect.height()):
                    self.addString(rect.x()+i,rect.y()+j," ")

    #def clear(self,x,y,width,height):
    #    for i in range(0,width):
    #        for j in range(0,height):
    #            self.addString(x+i,y+j," ")

    def drawChar(self,x,y,mapping,default,isBold=False):
        existing = self.readChar(x,y)
        if existing in mapping:
            char = mapping[existing]
        else:
            char = default
        self.addString(x,y,char,isBold)

    #                 ─        │        ┌        ┐        └        ┘        ├        ┤        ┬        ┴        ┼
    verticalMap   = {"─":"┼",          "┌":"├", "┐":"┤", "└":"├", "┘":"┤", "├":"├", "┤":"┤", "┬":"┼", "┴":"┼", "┼":"┼"}

    def drawVerticalLine(self,x,fro=0,to=None,inclusive=True,isBold=False):
        if to==None:
            to,_ = self.window.getmaxyx()
            to -= 1
        maxY = max(fro,to)
        minY = min(fro,to)
        if not inclusive:
            minY += 1
            maxY -= 1
        for i in range(minY,maxY+1):
            self.drawChar(x,i,Context.verticalMap,"│",isBold)

    #                 ─        │        ┌        ┐        └        ┘        ├        ┤        ┬        ┴        ┼
    horizontalMap = {         "│":"┼", "┌":"┬", "┐":"┬", "└":"┴", "┘":"┴", "├":"┼", "┤":"┼", "┬":"┬", "┴":"┴", "┼":"┼"}

    def drawHorizontalLine(self,y,fro=0,to=None,inclusive=True,isBold=False):
        if to==None:
            _,to = self.window.getmaxyx()
            to -= 1
        maxX = max(fro,to)
        minX = min(fro,to)
        if not inclusive:
            minX += 1
            maxX -= 1
        for i in range(minX,maxX+1):
            self.drawChar(i,y,Context.horizontalMap,"─",isBold)

    def invalidateComponent(self,component):
        self.invalidatedRect.unionWith(component.getRect())

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
        print("Mouse clicked to x="+str(x)+" y="+str(y))

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

        selectedSet = set()
        for component in self.diagramComponent.allComponents():
            if component.isSelected:
                selectedSet.add(component)

        pressedOnSet = set()
        for component in self.diagramComponent.allComponents():
            if component.isOnMe(x,y):
                pressedOnSet.add(component)

        if len(pressedOnSet)>0:
            self.movingComponents = True

        if len(selectedSet.intersection(pressedOnSet))==0:
            for component in selectedSet:
                component.isSelected = False
                self.context.invalidateComponent(component)

            for component in pressedOnSet:
                component.isSelected = True
                self.context.invalidateComponent(component)

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
        raise "Not sure how this got called without mouseReleased being called first"

    def mouseReleased(self, x, y):
        if self.oldRect!=None:
            for component in self.diagramComponent.allComponents():
                if self.oldRect.isInside(component.getRect()):
                    component.isSelected = True
                else:
                    component.isSelected = False

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
        self.selectedComponents = set()
        for component in diagramComponent.allComponents():
            if component.isSelected:
                self.selectedComponents.add(component)

    def mousePressed(self, x, y):
        raise "Not sure how this got called without mouseReleased being called first"

    def mouseReleased(self, x, y):
        self.editor.setState(IdleState(self.editor,self.context,self.diagramComponent))

    def mouseMoved(self, x, y):
        newPoint = Point(x,y)
        offset = newPoint - self.lastPoint
        for component in self.selectedComponents:
            self.context.invalidateComponent(component)
            oldLocation = component.getRect().topLeft()
            component.move(oldLocation + offset)
            self.context.invalidateComponent(component)

        self.lastPoint = newPoint



def createTestDiagram():
    diagramElement = Diagram()
    #context.drawVerticalLine(20)
    #context.drawVerticalLine(25)
    #context.drawVerticalLine(34)
    #context.drawHorizontalLine(10)
    #context.drawHorizontalLine(12)
    #context.drawHorizontalLine(15)
    textBoxElement1 = testTextBox()
    textBoxElement1.x = 20
    textBoxElement1.y = 10
    diagramElement.elements.append(textBoxElement1)

    textBoxElement2 = testTextBox()
    textBoxElement2.x = 60
    textBoxElement2.y = 20
    diagramElement.elements.append(textBoxElement2)


    fromConnectionPoint1 = ConnectionPoint()
    fromConnectionPoint1.element = textBoxElement1
    fromConnectionPoint1.side = Side.RIGHT
    fromConnectionPoint1.where = 0.5
    fromConnectionPoint1.end = End.NONE

    toConnectionPoint1 = ConnectionPoint()
    toConnectionPoint1.element = textBoxElement2
    toConnectionPoint1.side = Side.LEFT
    toConnectionPoint1.where = 0.25
    toConnectionPoint1.end = End.TRIANGLE

    connectorElement1 = ConnectorElement()
    connectorElement1.fromConnection = fromConnectionPoint1
    connectorElement1.toConnection = toConnectionPoint1
    connectorElement1.controlPoints.append(45)
    diagramElement.elements.append(connectorElement1)

    fromConnectionPoint2 = ConnectionPoint()
    fromConnectionPoint2.element = textBoxElement1
    fromConnectionPoint2.side = Side.BOTTOM
    fromConnectionPoint2.where = 0.75
    fromConnectionPoint2.end = End.ARROW

    toConnectionPoint2 = ConnectionPoint()
    toConnectionPoint2.element = textBoxElement2
    toConnectionPoint2.side = Side.TOP
    toConnectionPoint2.where = 0.5
    toConnectionPoint2.end = End.NONE

    connectorElement2 = ConnectorElement()
    connectorElement2.fromConnection = fromConnectionPoint2
    connectorElement2.toConnection = toConnectionPoint2
    connectorElement2.controlPoints.append(19)
    connectorElement2.controlPoints.append(51)
    connectorElement2.controlPoints.append(15)
    diagramElement.elements.append(connectorElement2)

    return diagramElement

def createDiagramComponent(diagramElement):
    diagramComponent = DiagramComponent(diagramElement)

    for element in diagramElement.elements:
        if type(element) is TextBoxElement:
            component = TextBoxComponent(element)
        elif type(element) is ConnectorElement:
            component = ConnectorComponent(element)

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
            if event == ord('q'):
                break
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


mystdout = StdOutWrapper()
sys.stdout = mystdout
sys.stderr = mystdout

try:
    wrapper(myMain)
finally:

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())
    sys.stdout.write("\n")
