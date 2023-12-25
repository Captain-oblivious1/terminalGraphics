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
        rect = self.rectElement.rect
        l = rect.l
        r = rect.r-1
        t = rect.t
        b = rect.b-1
        context.orChar(l,t,'┌',False)
        context.orChar(r,t,'┐',False)
        context.orChar(l,b,'└',False)
        context.orChar(r,b,'┘',False)
        l += 1
        t += 1
        r -= 1
        b -= 1
        context.drawVerticalLine(l-1,t,b,False)
        context.drawVerticalLine(r+1,t,b,False)
        context.drawHorizontalLine(t-1,l,r,False)
        context.drawHorizontalLine(b+1,l,r,False)

    # Default is for entier rectangle to be true
    def isOnMe(self,point):
        rect = self.rectElement.rect
        l = rect.l
        r = rect.r-1
        t = rect.t
        b = rect.b-1
        return point.x==l or point.x==r or point.y==t or point.y==b

    def move(self,offset,context):
        oldRect = self.rectElement.rect
        newRect = Rect(oldRect.l+offset.x,oldRect.t+offset.y,oldRect.width(),oldRect.height())
        print("oldRect="+str(oldRect)+" newRect="+str(newRect))
        self.rectElement.rect = newRect
