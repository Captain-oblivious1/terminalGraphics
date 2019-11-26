from enum import Enum
from Model import *
import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,right):
        return Point(self.x+right.x,self.y+right.y)

    def __iadd__(self,right):
        self.x += right.x
        self.y += right.y
        return self

    def __sub__(self,right):
        return Point(self.x-right.x,self.y-right.y)

    def __str__(self):
        return "Point("+str(self.x)+","+str(self.y)+")"

class Rect:
    def __init__(self,x=math.inf,y=math.inf,width=-math.inf,height=-math.inf):
        self.l,self.r = Rect._initDim(x,width)
        self.t,self.b = Rect._initDim(y,height)

    def _initDim(pos,length):
        if length==-math.inf:
            return pos,-math.inf  #cannot do ∞-∞.  So returning max of -∞
        elif length<0:
            return pos+length, pos  #always want min to be less than max (i.e. no negative width allowed)
        else:
            return pos, pos+length

    def makeRectFromPoints(topLeft,bottomRight):
        return Rect(
                topLeft.x,
                topLeft.y,
                bottomRight.x-topLeft.x+1,
                bottomRight.y-topLeft.y+1)

    def includePoint(self,point):
        rect = Rect(point.x,point.y,1,1)
        self.unionWith(rect)
        return self

    def unionWith(self,rect):
        self.l = min(self.l,rect.l)
        self.t = min(self.t,rect.t)
        self.r = max(self.r,rect.r)
        self.b = max(self.b,rect.b)
        return self

    def doesIntersect(self,rect):
        return self.l <= rect.r and self.r > rect.l and self.t <= rect.b and self.b > rect.t

    def isNullRect(self):
        return self.l==math.inf or self.t==math.inf or self.r==-math.inf or self.b==-math.inf

    def isInsideRect(self,amIInside):
        return self.l<=amIInside.l and self.r>amIInside.r and self.t<=amIInside.t and self.b>amIInside.b

    def isInsidePoint(self,amIInside):
        return self.l<=amIInside.x and self.r>amIInside.x and self.t<=amIInside.y and self.b>amIInside.y

    def x(self):
        return self.l

    def y(self):
        return self.t

    def width(self):
        return self.r-self.l

    def height(self):
        return self.b-self.t

    def topLeft(self):
        return Point(self.l,self.t)

    def bottomRight(self):
        return Point(self.r,self.b)

    #def area(self):
    #    return self.width()*self.height()

    def __str__(self):
        return "Rect:{x="+str(self.l)+",y="+str(self.t)+",width="+str(self.width())+",height="+str(self.height())+"}"

def testRect():
    print("inf="+str(math.inf-math.inf))
    print(Rect(5,10,45,30).unionWith(Rect(20,20,50,25)))
    print(Rect(25,30,10,10).unionWith(Rect(20,20,50,25)))
    print(Rect().unionWith(Rect(20,20,50,25)))


def isHorizontal(side):
    return side == Direction.LEFT or side == Direction.RIGHT

class Component:
    def __init__(self, element):
        self.element = element
        self.selected = False

    def getRect(self):
        return Rect()

    def isSelected(self):
        return self.selected

    def setSelected(self,newSelected):
        self.selected = newSelected

    def children(self):
        return set()

    def isOnMe(self,point):
        return self.getRect().isInsidePoint(point)

class BoxComponent(Component):
    # These maps are so that when a box is drawn on top of other things, it doesn't look bad
    #
    # So like this:    │        Not this:    │
    #               ┌──┴──┐               ┌─────┐
    #             ──┤ box ├──           ──│ box │──
    #               └──┬──┘               └─────┘
    #                  │                     │
    #
    # So for example, when drawing the top part of a box, and it's about to draw over an existing "│" with "─", it
    # will first check the topMap and find the "│" as a key and will draw the corresponding "┴" value instead.
    #
    #                  ─        │        ┌        ┐        └        ┘        ├        ┤        ┬        ┴        ┼
    topMap    =      {         "│":"┴",                   "└":"┴", "┘":"┴", "├":"┴", "┤":"┴",          "┴":"┴", "┼":"┴"}
    bottomMap =      {         "│":"┬", "┌":"┬", "┐":"┬",                   "├":"┬", "┤":"┬", "┬":"┬",          "┼":"┬"}
    leftMap   =      {"─":"┤",                   "┐":"┤",          "┘":"┤",          "┤":"┤", "┬":"┤", "┴":"┤", "┼":"┤"}
    rightMap  =      {"─":"├",          "┌":"├",          "└":"├",          "├":"├",          "┬":"├", "┴":"├", "┼":"├"}

    topLeftMap     = {"─":"┬", "│":"├",          "┐":"┬", "└":"├", "┘":"┼", "├":"├", "┤":"┼", "┬":"┬", "┴":"┼", "┼":"┼"}
    topRightMap    = {"─":"┬", "│":"┤", "┌":"┬",          "└":"┤", "┘":"┤", "├":"┼", "┤":"┤", "┬":"┬", "┴":"┼", "┼":"┼"}
    bottomLeftMap  = {"─":"┴", "│":"├", "┌":"├", "┐":"┼",          "┘":"┴", "├":"├", "┤":"┼", "┬":"┼", "┴":"┴", "┼":"┼"}
    bottomRightMap = {"─":"┴", "│":"┤", "┌":"┼", "┐":"┤", "└":"┴", "┘":"┘", "├":"┼", "┤":"┤", "┬":"┼", "┴":"┴", "┼":"┼"}

    def __init__(self,boxElement):
        Component.__init__(self,boxElement)

    def _drawBorderChar(self,context,x,y,mapping,default):
        context.drawChar(x,y,mapping,default,self.isSelected())

    def draw(self,context):
        x = self.element.x
        y = self.element.y
        width = self.element.width
        height = self.element.height
        height -= 1
        width -= 1
        bottom = y+height
        right = x+width

        for i in range(1,width):
            self._drawBorderChar(context,x+i,y,TextBoxComponent.topMap,"─")
            self._drawBorderChar(context,x+i,bottom,TextBoxComponent.bottomMap,"─")

        for i in range(1,height):
            self._drawBorderChar(context,x,y+i,TextBoxComponent.leftMap,"│")
            self._drawBorderChar(context,right,y+i,TextBoxComponent.rightMap,"│")

        self._drawBorderChar(context,x,y,TextBoxComponent.topLeftMap,"┌")
        self._drawBorderChar(context,right,y,TextBoxComponent.topRightMap,"┐")
        self._drawBorderChar(context,x,bottom,TextBoxComponent.bottomLeftMap,"└")
        self._drawBorderChar(context,right,bottom,TextBoxComponent.bottomRightMap,"┘")

        context.clearRect(Rect(x+1,y+1,width-1,height-1))

    def getRect(self):
        return Rect(self.element.x,self.element.y,self.element.width,self.element.height)

    def move(self,offset):
        element = self.element
        element.x += offset.x
        element.y += offset.y

class TextBoxComponent(BoxComponent):
    def __init__(self,textBoxElement):
        BoxComponent.__init__(self,textBoxElement)

    def draw(self,context):
        BoxComponent.draw(self,context)
        x = self.element.x
        y = self.element.y
        width = self.element.width
        height = self.element.height
        height -= 1
        width -= 2

        row = y+1
        for line in self.element.lines:
            lineLength = len(line.text)
            if line.justification == Justification.LEFT:
                col = x + 1
            elif line.justification == Justification.CENTER:
                col = x + int(width/2-lineLength/2) + 1
            elif line.justification == Justification.RIGHT:
                col = x + width - lineLength + 1

            context.addString(col,row,line.text,self.isSelected())
            row += 1

class DiagramComponent(Component):
    def __init__(self,diagramElement):
        Component.__init__(self,diagramElement)
        self.components = []
        self.selectionRect = None

    def invalidateAll(self,context):
        for component in self.components:
            context.invalidateComponent(component)

    def draw(self,context):
        invalidatedRect = context.getInvalidatedRect()
        context.clearRect(invalidatedRect)

        for component in self.components:
            #print("testing intesection of "+str(component.getRect())+" and "+str(invalidatedRect))
            if component.getRect().doesIntersect(invalidatedRect):
                #print("Found intersection")
                component.draw(context)

        if self.selectionRect!=None:
            for col in range(self.selectionRect.l,self.selectionRect.r):
                for row in range(self.selectionRect.t,self.selectionRect.b):
                    char = context.readChar(col,row)
                    #print("char='"+char+"' ord="+hex(ord(char)))
                    context.addString(col,row,char,False,True)

    def children(self):
        return self.components

    def setSelectionRect(self,rect):
        self.selectionRect = rect

    def allSelectedComponent(component,theSet):
        if component.isSelected():
            theSet.add(component)
        for child in component.children():
            DiagramComponent.allSelectedComponent(child,theSet)

    def allSelected(self):
        returnMe = set()
        DiagramComponent.allSelectedComponent(self,returnMe)
        return returnMe

    def componentAt(component,point):
        #print("testing at point="+str(point))  (51,17)
        for child in component.children():
            found = DiagramComponent.componentAt(child,point)
            #print("testing child="+str(child)+" found="+str(found))
            if found!=None:
                return found

        if component.isOnMe(point):
            return component
        else:
            return None

    def isOnMe(self, point):
        return False
