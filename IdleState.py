from State import *
#from MovingState import *
from Point import *
from Menu import *
from TextComponent import *
from PathComponent import *
from Model import *

class IdleState(State):
    def __init__(self,editor,context,diagramComponent):
        self.editor = editor
        self.context = context
        self.diagramComponent = diagramComponent
        self.startDragPoint = None
        self.movingComponents = False
        self.clickedOn = None

    def mousePressed(self, x, y):
        # Curses does not support testing of shift, ctrl, alt, etc.  So I can't 
        # pretend I'm powerpoint here

        self.startDragPoint = Point(x,y)

        selectedSet = self.diagramComponent.allSelected()

        clickedOn = self.diagramComponent.componentAt(self.startDragPoint)

        if clickedOn==None or not clickedOn in selectedSet:
            for component in selectedSet:
                component.setSelected(False)
                component.invalidate()

        if clickedOn!=None:
            if "clickedOn" in dir(clickedOn):
                self.clickedOn = clickedOn

            self.movingComponents = True
            clickedOn.setSelected(True)
            #print("Invalidating clicked on")
            clickedOn.invalidate()


    def mouseReleased(self, x, y):
        self.startDragPoint = None
        self.movingComponents = False
        if self.clickedOn!=None:
            self.clickedOn.clickedOn(Point(x,y))
        self.clickedOn = None

    def mouseMoved(self, x, y):
        if self.startDragPoint!=None:
            if self.movingComponents:
                self.editor.goMovingState(self.startDragPoint)
            else:
                self.editor.goLassoState(self.startDragPoint)

    def rightReleased(self, x, y):
        point = Point(x,y)
        clickedOn = self.diagramComponent.componentAt(point)
        if clickedOn!=None:
            if "showContextMenu" in dir(clickedOn):
                clickedOn.showContextMenu(point,self.context)
        else:
            self.showContextMenu(point)

    def showContextMenu(self,point):
        options = ["Add text","Add path"]
        self.diagramComponent.showMenu(Menu(self.diagramComponent,options,point,self.menuResult))

    def menuResult(self,menu):
        option = menu.getSelectedOption()
        if option=="Add text":
            textElement = TextElement()
            textElement.text = "New text"
            textElement.location = menu.topLeft
            textElement.justification = Justification.LEFT
            self.diagramComponent.addComponent(TextComponent(self.diagramComponent,textElement))
        elif option=="Add path":
            pathElement = PathElement()
            pathElement.pathType = PathType.CLOSED
            pathElement.fill = Fill.OPAQUE
            pathElement.startOrientation = Orientation.HORIZONTAL
            p = menu.topLeft
            pathElement.turns = [p.x,p.y,p.x+5,p.y+3]
            pathElement.corners = Corners.ROUND
            self.diagramComponent.addComponent(PathComponent(self.diagramComponent,pathElement))
