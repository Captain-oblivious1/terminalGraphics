from Component import *

from Rect import *
from Menu import *
from Model import *

class SequenceComponent(Component):
    def __init__(self,parent,element):
        super().__init__(parent)
        self.element = element

    def getRect(self):
        actors = self.element.actors
        lenActors = len(actors)
        if lenActors>0:
            l = actors[0].x - int(len(actors[0].label)/2) - 1
            r = actors[-1].x + int(len(actors[1].label)/2) + 1
            t = self.element.top
            b = 0
            lines = self.element.lines
            for line in lines:
                b = max(line.y,b)

            rect = Rect(l,t,r-l+1,b-t+1)
        else:
            rect = Rect()

        return rect

    def draw(self,context):
        selected = self.isSelected()
        element = self.element

        bottom = 0
        lines = self.element.lines
        for line in lines:
            bottom = max(line.y,bottom)

        actors = element.actors
        for actor in actors:
            lenLabel = len(actor.label)
            l = actor.x - int(lenLabel/2) - 1
            r = l + lenLabel + 1
            t = element.top
            _,n = longestLineAndNumberLines(actor.label)
            b = t + n + 1
            rect = Rect()
            rect.l = l
            rect.r = r
            rect.t = t
            rect.b = b
            context.drawVerticalLine(actor.x,b,bottom,Thickness.THIN,Style.SOLID,selected)
            context.drawFilledBox(rect,selected)
            context.writeString(l+1,t+1,actor.label)

        for line in lines:
            y = line.y
            fx = actors[line.fro].x
            tx = actors[line.to].x
            if fx<tx:
                context.writeString(tx-1,y,'>')
                context.orChar(fx,y,'╶')
                fx += 1
                tx -= 2
            else:
                context.writeString(tx+1,y,'<')
                context.orChar(fx,y,'╴')
                fx -= 1
                tx += 2

            context.drawHorizontalLine(y,fx,tx,Thickness.THIN,Style.SOLID,selected)

            

    ## Default is for entier rectangle to be true
    #def isOnMe(self,point):
    #    rect = self.rectElement.rect
    #    l = rect.l
    #    r = rect.r-1
    #    t = rect.t
    #    b = rect.b-1
    #    return point.x==l or point.x==r or point.y==t or point.y==b

    def move(self,fromPoint,offset,context):
        oldRect = self.element.rect
        newRect = Rect(oldRect.l+offset.x,oldRect.t+offset.y,oldRect.width(),oldRect.height())
        self.element.rect = newRect

    def showContextMenu(self,point,context):
        options = ["stop editing","","split","join"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        print("Chose menu option '"+menu.getSelectedOption()+"'")
