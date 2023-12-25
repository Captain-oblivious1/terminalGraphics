from enum import Enum
from Model import *
from Rect import *
import math

def isHorizontal(side):
    return side == Direction.LEFT or side == Direction.RIGHT

class Component:
    def __init__(self, parent):
        self.parent = parent
        self.selected = False

    def getEditor(self):
        return self.parent.getEditor()

    def getRect(self):
        return Rect()

    def isSelected(self):
        return self.selected

    def setSelected(self,newSelected):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! setting selected (this="+str(self)+")="+str(newSelected))
        self.selected = newSelected

    def children(self):
        return set()

    def isOnMe(self,point):
        return True  #this is only called if point is within bounding rect.

    def getTopLevelComponent(self):
        if self.parent==None:
            return self
        else:
            return self.parent.getTopLevelComponent()

    def getDiagramComponent(self):
        return self.getTopLevelComponent()

    def invalidate(self):
        self.getEditor().getContext().invalidateRect( self.getRect() )

    #def getDiagram(

#class BoxComponent(Component):
#    # These maps are so that when a box is drawn on top of other things, it doesn't look bad
#    #
#    # So like this:    │        Not this:    │
#    #               ┌──┴──┐               ┌─────┐
#    #             ──┤ box ├──           ──│ box │──
#    #               └──┬──┘               └─────┘
#    #                  │                     │
#    #
#    # So for example, when drawing the top part of a box, and it's about to draw over an existing "│" with "─", it
#    # will first check the topMap and find the "│" as a key and will draw the corresponding "┴" value instead.
#    #
#    #                  ─        │        ┌        ┐        └        ┘        ├        ┤        ┬        ┴        ┼
#    #topMap    =      {         "│":"┴",                   "└":"┴", "┘":"┴", "├":"┴", "┤":"┴",          "┴":"┴", "┼":"┴"}
#    #bottomMap =      {         "│":"┬", "┌":"┬", "┐":"┬",                   "├":"┬", "┤":"┬", "┬":"┬",          "┼":"┬"}
#    #leftMap   =      {"─":"┤",                   "┐":"┤",          "┘":"┤",          "┤":"┤", "┬":"┤", "┴":"┤", "┼":"┤"}
#    #rightMap  =      {"─":"├",          "┌":"├",          "└":"├",          "├":"├",          "┬":"├", "┴":"├", "┼":"├"}
#
#    #topLeftMap     = {"─":"┬", "│":"├",          "┐":"┬", "└":"├", "┘":"┼", "├":"├", "┤":"┼", "┬":"┬", "┴":"┼", "┼":"┼"}
#    #topRightMap    = {"─":"┬", "│":"┤", "┌":"┬",          "└":"┤", "┘":"┤", "├":"┼", "┤":"┤", "┬":"┬", "┴":"┼", "┼":"┼"}
#    #bottomLeftMap  = {"─":"┴", "│":"├", "┌":"├", "┐":"┼",          "┘":"┴", "├":"├", "┤":"┼", "┬":"┼", "┴":"┴", "┼":"┼"}
#    #bottomRightMap = {"─":"┴", "│":"┤", "┌":"┼", "┐":"┤", "└":"┴", "┘":"┘", "├":"┼", "┤":"┤", "┬":"┼", "┴":"┴", "┼":"┼"}
#
#    def __init__(self,boxElement):
#        Component.__init__(self,boxElement)
#
#    def draw(self,context):
#        x = self.element.x
#        y = self.element.y
#        width = self.element.width
#        height = self.element.height
#        height -= 1
#        width -= 1
#        bottom = y+height
#        right = x+width
#
#        selected = self.isSelected()
#        for i in range(1,width):
#            context.andChar(x+i,y,"▀")
#            context.orChar(x+i,y,"─",selected)
#            context.andChar(x+i,bottom,"▄")
#            context.orChar(x+i,bottom,"─",selected)
#            #self._drawBorderChar(context,x+i,y,TextBoxComponent.topMap,"─")
#            #self._drawBorderChar(context,x+i,bottom,TextBoxComponent.bottomMap,"─")
#
#        for i in range(1,height):
#            context.andChar(x,y+i,"▌")
#            context.orChar(x,y+i,"│",selected)
#            context.andChar(right,y+i,"▐")
#            context.orChar(right,y+i,"│",selected)
#            #self._drawBorderChar(context,x,y+i,TextBoxComponent.leftMap,"│")
#            #self._drawBorderChar(context,right,y+i,TextBoxComponent.rightMap,"│")
#
#        context.andChar(x,y,"▛")
#        context.orChar(x,y,"┌",selected)
#        context.andChar(right,y,"▜")
#        context.orChar(right,y,"┐",selected)
#        context.andChar(x,bottom,"▙")
#        context.orChar(x,bottom,"└",selected)
#        context.andChar(right,bottom,"▟")
#        context.orChar(right,bottom,"┘",selected)
#        #self._drawBorderChar(context,x,y,TextBoxComponent.topLeftMap,"┌")
#        #self._drawBorderChar(context,right,y,TextBoxComponent.topRightMap,"┐")
#        #self._drawBorderChar(context,x,bottom,TextBoxComponent.bottomLeftMap,"└")
#        #self._drawBorderChar(context,right,bottom,TextBoxComponent.bottomRightMap,"┘")
#
#        context.clearRect(Rect(x+1,y+1,width-1,height-1))
#
#    def getRect(self):
#        return Rect(self.element.x,self.element.y,self.element.width,self.element.height)
#
#    def move(self,offset,context):
#        element = self.element
#        element.x += offset.x
#        element.y += offset.y
#
#class TextBoxComponent(BoxComponent):
#    def __init__(self,textBoxElement):
#        BoxComponent.__init__(self,textBoxElement)
#
#    def draw(self,context):
#        BoxComponent.draw(self,context)
#        x = self.element.x
#        y = self.element.y
#        width = self.element.width
#        height = self.element.height
#        height -= 1
#        width -= 2
#
#        row = y+1
#        for line in self.element.lines:
#            lineLength = len(line.text)
#            if line.justification == Justification.LEFT:
#                col = x + 1
#            elif line.justification == Justification.CENTER:
#                col = x + int(width/2-lineLength/2) + 1
#            elif line.justification == Justification.RIGHT:
#                col = x + width - lineLength + 1
#
#            context.addString(col,row,line.text,self.isSelected())
#            row += 1
