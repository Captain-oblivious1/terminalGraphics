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

        if clickedOn==None:
            menu = self.diagramComponent.menu
            if menu is not None:
                menu.invalidate()
                self.diagramComponent.menu = None
        else:
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
        options = ["add text","add closed path","add HH path","add HV path","add VV path","add table"]
        self.diagramComponent.showMenu(Menu(self.diagramComponent,options,point,self.menuResult))

    def menuResult(self,menu):
        option = menu.getSelectedOption()
        if option=="add text":
            textElement = TextElement()
            textElement.text = "New text"
            textElement.location = menu.topLeft
            textElement.justification = Justification.LEFT
            self.diagramComponent.addElement(textElement)
        elif option=="add closed path":
            pathElement = PathElement()
            pathElement.pathType = PathType.CLOSED
            pathElement.fill = Fill.OPAQUE
            pathElement.startOrientation = Orientation.HORIZONTAL
            p = menu.topLeft
            pathElement.turns = [p.x,p.y,p.x+10,p.y+3]
            pathElement.corners = Corners.ROUND
            self.diagramComponent.addElement(pathElement)
        elif option=="add HH path":
            pathElement = PathElement()
            pathElement.pathType = PathType.OPEN
            pathElement.startOrientation = Orientation.HORIZONTAL
            p = menu.topLeft
            pathElement.turns = [p.x,p.y,p.x+5]
            pathElement.corners = Corners.ROUND
            pathElement.startArrow = Arrow.NONE
            pathElement.endArrow = Arrow.TRIANGLE
            self.diagramComponent.addElement(pathElement)
        elif option=="add HV path":
            pathElement = PathElement()
            pathElement.pathType = PathType.OPEN
            pathElement.startOrientation = Orientation.HORIZONTAL
            p = menu.topLeft
            pathElement.turns = [p.x,p.y,p.x+5,p.y+3]
            pathElement.corners = Corners.ROUND
            pathElement.startArrow = Arrow.NONE
            pathElement.endArrow = Arrow.TRIANGLE
            self.diagramComponent.addElement(pathElement)
        elif option=="add VV path":
            pathElement = PathElement()
            pathElement.pathType = PathType.OPEN
            pathElement.startOrientation = Orientation.VERTICAL
            p = menu.topLeft
            pathElement.turns = [p.y,p.x,p.y+5]
            pathElement.corners = Corners.ROUND
            pathElement.startArrow = Arrow.NONE
            pathElement.endArrow = Arrow.TRIANGLE
            self.diagramComponent.addElement(pathElement)
        elif option=="add table":
            p = menu.topLeft
            tableElement = TableElement()
            tableElement.location = p
            tableElement.columnWidths = [5]
            tableElement.rowHeights = [1,1]
            one = TableField()
            one.text = "Your"
            one.justification = Justification.CENTER
            two = TableField()
            two.text = "table"
            two.justification = Justification.CENTER
            tableElement.dataRows = [ [ one ] , [ two ] ]
            self.diagramComponent.addElement(tableElement)
