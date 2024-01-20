import curses

from Component import *
from Rect import *
from Menu import *
from Model import *

class SequenceComponent(Component):
    def __init__(self,parent,element):
        super().__init__(parent)
        self.element = element
        self.selectedActor = None
        self.selectedLine = None
        self.drawingLine = None

    def setSelected(self,newSelected):
        super().setSelected(newSelected)
        editor = self.getEditor()
        if newSelected is not None:
            editor.addKeyListener(self)
        else:
            editor.removeKeyListener(self)

        self.selected = newSelected

    def getRect(self):
        element = self.element
            
        rect = Rect()
        for actor in element.actors:
            rect.unionWith(self._rectForBox(actor))

        for line in element.lines:
            rect.b = max(rect.b,line.y)

        if self.drawingLine!=None:
            rect.b = max(rect.b,self.drawingLine.y)

        rect.r += 1
        rect.b += 1

        return rect

    def draw(self,context):
        selected = self.isSelected()
        element = self.element

        bottom = 0
        if self.drawingLine!=None:
            lines = [self.drawingLine] + element.lines
        else:
            lines = element.lines

        for line in lines:
            bottom = max(line.y,bottom)

        actors = element.actors
        for actor in actors:
            rect = self._rectForBox(actor)
            meSelected = self.selectedActor==actor or self.selectedActor==None and selected
            context.drawVerticalLine(actor.x,rect.b,bottom,Thickness.THIN,Style.SOLID,meSelected)
            context.drawFilledBox(rect,meSelected)
            context.writeString(rect.l+1,rect.t+1,actor.label)

        for line in lines:
            meSelected = self.selectedLine==line or self.selectedLine==None and selected
            self._drawLine(context,line,meSelected)

    def _drawLine(self,context,line,selected):
        actors = self.element.actors
        y = line.y
        fx = actors[line.fro].x
        tx = actors[line.to].x
        if fx<tx:
            context.writeString(tx-1,y,'>',selected)
            context.orChar(fx,y,'╶',selected)
            fx += 1
            tx -= 2
        else:
            context.writeString(tx+1,y,'<',selected)
            context.orChar(fx,y,'╴',selected)
            fx -= 1
            tx += 2

        context.drawHorizontalLine(y,fx,tx,Thickness.THIN,Style.SOLID,selected)

    def _rectForBox(self,actor):
        lenLabel = len(actor.label)
        l = actor.x - int(lenLabel/2) - 1
        r = l + lenLabel + 1
        t = self.element.top
        _,n = longestLineAndNumberLines(actor.label)
        b = t + n + 1
        rect = Rect()
        rect.l = l
        rect.r = r
        rect.t = t
        rect.b = b
        return rect

    ## Default is for entier rectangle to be true
    #def isOnMe(self,point):
    #    rect = self.rectElement.rect
    #    l = rect.l
    #    r = rect.r-1
    #    t = rect.t
    #    b = rect.b-1
    #    return point.x==l or point.x==r or point.y==t or point.y==b

    def startMove(self,point,context):
        self.selectedActor = self._actorAt(point)
        self.selectedLine = self._lineAt(point)
        if self.selectedActor is not None or self.selectedLine is not None:
            self.setSelected(False)

    def move(self,fromPoint,offset,context):
        element = self.element
        actors = element.actors

        if self.selectedActor != None:
            self.selectedActor.x += offset.x
            return

        if self.selectedLine != None:
            self.selectedLine.y += offset.y
            return

        for actor in actors:
            actor.x += offset.x

        element.top += offset.y
        for line in self.element.lines:
            line.y += offset.y

    def finishMove(self,point,context):
        pass

    def _actorAt(self,point):
        for actor in self.element.actors:
            if actor.x==point.x:
                return actor
            rect = self._rectForBox(actor)
            rect.r += 1
            rect.b += 1
            if rect.isInsidePoint(point):
                return actor
        return None

    def _lineAt(self,point):
        actors = self.element.actors
        for line in self.element.lines:
            fromActor = actors[line.fro]
            toActor = actors[line.to]
            left = min(fromActor.x,toActor.x)
            right = max(fromActor.x,toActor.x)
            x = point.x
            if x>=left and x<=right and point.y==line.y:
                return line

    def mouseEvent(self,event):
        _ , mx, my, _, bstate = curses.getmouse()
        if self.getRect().isInsidePoint( Point(mx,my) ):
            actors = self.element.actors
            lActors = len(actors)
            if lActors>0:
                self.invalidate()
                closestIndex = 0
                minDist = abs(actors[0].x-mx)
                for i in range(1,len(actors)):
                    actor = actors[i]
                    x = actor.x
                    dist = abs(x-mx)
                    if dist<minDist:
                        minDist = dist
                        closestIndex = i
                self.drawingLine.to = closestIndex
                self.drawingLine.y = my
                self.invalidate()

            if bstate & curses.BUTTON1_RELEASED != 0:
                self.element.lines.append(self.drawingLine)
                self.selectedLine = self.drawingLine = None
                self.getEditor().removeMouseListener(self)
            return True
        else:
            return False

    def keyEvent(self,event):
        print("got key event="+str(event))
        if event == 330:  # del key
            self._delete()
            return True
        else:
            return False

    def _delete(self):
        self.invalidate()
        element = self.element
        if self.selectedLine is not None:
            element.lines.remove(self.selectedLine)
        if self.selectedActor is not None:
            index = element.actors.index(self.selectedActor)
            print("index="+str(index))
            for line in element.lines.copy():
                if line.fro==index or line.to==index:
                    print("deleting line="+str(index))
                    element.lines.remove(line)
                else:
                    if line.fro>index:
                        line.fro -= 1
                    if line.to>index:
                        line.to -= 1

            self.element.actors.remove(self.selectedActor)
        self.invalidate()

    def showContextMenu(self,point,context):
        actor = self._actorAt(point)
        if actor != None:
            options = ["add line from"]
        else:
            options = ["add actor"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        option = menu.getSelectedOption()
        if option=="add actor":
            actor = Actor()
            actor.label = "new actor"
            actor.x = menu.topLeft.x
            self.element.actors.append(actor)
            self.invalidate()
        elif option=="add line from": 
            actorFrom = self._actorAt(menu.topLeft)
            drawingLine = Line()
            drawingLine.y = menu.topLeft.y
            index = self.element.actors.index(actorFrom)
            drawingLine.fro = index
            drawingLine.to = index
            self.selectedLine = self.drawingLine = drawingLine
            self.getEditor().addMouseListener(self)
