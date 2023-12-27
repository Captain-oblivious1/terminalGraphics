from Component import *

from Util import *
from Rect import *
from Menu import *
from Model import *

class RectElement(Element):
    def __init__(self,rect):
        self.rect = rect

class RectComponent(Component):
    def __init__(self,parent,rectElement):
        super().__init__(parent)
        self.rectElement = rectElement

    def getRect(self):
        return self.rectElement.rect

    def draw(self,context):
        selected = self.isSelected()
        #print("selected="+str(selected))
        rect = self.rectElement.rect
        l = rect.l
        r = rect.r-1
        t = rect.t
        b = rect.b-1
        context.orChar(l,t,'┌',selected)
        context.orChar(r,t,'┐',selected)
        context.orChar(l,b,'└',selected)
        context.orChar(r,b,'┘',selected)
        l += 1
        t += 1
        r -= 1
        b -= 1
        context.drawVerticalLine(l-1,t,b,selected)
        context.drawVerticalLine(r+1,t,b,selected)
        context.drawHorizontalLine(t-1,l,r,selected)
        context.drawHorizontalLine(b+1,l,r,selected)

    # Default is for entier rectangle to be true
    def isOnMe(self,point):
        rect = self.rectElement.rect
        l = rect.l
        r = rect.r-1
        t = rect.t
        b = rect.b-1
        return point.x==l or point.x==r or point.y==t or point.y==b

    def move(self,fromPoint,offset,context):
        oldRect = self.rectElement.rect
        newRect = Rect(oldRect.l+offset.x,oldRect.t+offset.y,oldRect.width(),oldRect.height())
        self.rectElement.rect = newRect

    def showContextMenu(self,point,context):
        options = ["stop editing","","split","join"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        print("Chose menu option '"+menu.getSelectedOption()+"'")
