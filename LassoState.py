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
                if self.oldRect.isInsideRect(component.getRect(),True):
                    component.setSelected(True)
                else:
                    component.setSelected(False)

            context = self.diagramComponent.getEditor().getContext()
            context.invalidateRect(self.oldRect)
            self.diagramComponent.setSelectionRect(None)

        self.editor.goIdleState()

    def mouseMoved(self, x, y):
        startX=self.startDragPoint.x
        startY=self.startDragPoint.y

        topLeft = Point( min(startX,x), min(startY,y) )
        bottomRight = Point( max(startX,x), max(startY,y) )

        rect = Rect.makeRectFromPoints(topLeft,bottomRight)
        diagramComponent = self.diagramComponent
        editor = diagramComponent.getEditor()
        context = editor.getContext()
        diagramComponent.setSelectionRect(rect)
        context.invalidateRect(rect)
        if self.oldRect!=None:
            context.invalidateRect(self.oldRect)
        self.oldRect = rect


