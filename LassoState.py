from State import *
from Point import *
from Rect import *

class LassoState(State):
    def __init__(self,editor,context,diagramComponent,startDragPoint):
        self.editor = editor
        self.context = context
        self.diagramComponent = diagramComponent
        self.startDragPoint = startDragPoint
        self.oldRect = None

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        if self.oldRect!=None:
            for component in self.diagramComponent.children():
                if self.oldRect.isInsideRect(component.getRect()):
                    component.setSelected(True)
                else:
                    component.setSelected(False)

            self.diagramComponent.invalidateRect(self.oldRect)
            self.diagramComponent.setSelectionRect(None)

        self.editor.goIdleState()

    def mouseMoved(self, x, y):
        startX=self.startDragPoint.x
        startY=self.startDragPoint.y

        topLeft = Point( min(startX,x), min(startY,y) )
        bottomRight = Point( max(startX,x), max(startY,y) )

        rect = Rect.makeRectFromPoints(topLeft,bottomRight)
        self.diagramComponent.setSelectionRect(rect)
        self.diagramComponent.invalidateRect(rect)
        if self.oldRect!=None:
            self.diagramComponent.invalidateRect(self.oldRect)
        self.oldRect = rect


