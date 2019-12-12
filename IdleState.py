from State import *
#from MovingState import *
from Point import *

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
                component.invalidate()

        if clickedOn!=None:
            self.movingComponents = True
            clickedOn.setSelected(True)
            #print("Invalidating clicked on")
            clickedOn.invalidate()

    def mouseReleased(self, x, y):
        self.startDragPoint = None
        self.movingComponents = False

    def mouseMoved(self, x, y):
        if self.startDragPoint!=None:
            if self.movingComponents:
                self.editor.goMovingState(self.startDragPoint)
            else:
                self.editor.goLassoState(self.startDragPoint)

    def rightReleased(self, x, y):
        point = Point(x,y)
        clickedOn = self.diagramComponent.componentAt(point)
        if "showContextMenu" in dir(clickedOn):
            clickedOn.showContextMenu(point,self.context)



