#from IdleState import *
from State import *
from Point import *

class MovingState(State):
    def __init__(self,editor,context,diagramComponent,startDragPoint):
        self.editor = editor
        self.context = context
        self.diagramComponent = diagramComponent
        self.lastPoint = startDragPoint

        self.selectedComponents = diagramComponent.allSelected()
        for component in self.selectedComponents:
            if "startMove" in dir(component):
                component.startMove(startDragPoint,context)

        #selectedElements = set()
        #for component in self.selectedComponents:
        #    if "getElement" in dir(component)
        #        selectedElements.add(component.getElement())

        #self.affectedConnectors = set()
        #for component in self.diagramComponent.children():
        #    if issubclass(type(component),ConnectorComponent):
        #        connectorElement = component.element
        #        if connectorElement.fromConnection.element in selectedElements or connectorElement.toConnection.element in selectedElements:
        #            self.affectedConnectors.add(component)

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        point = Point(x,y)
        for component in self.selectedComponents:
            if "finishMove" in dir(component):
                component.finishMove(point,self.context)

        self.editor.goIdleState()

    def mouseMoved(self, x, y):
        newPoint = Point(x,y)
        offset = newPoint - self.lastPoint
        if offset!=Point(0,0):

            ## Invalidate the location where the connectors were (to erase them if necessary)
            #for component in self.affectedConnectors:
            #    self.context.invalidateComponent(component)

            for component in self.selectedComponents:
                component.invalidate()
                component.move(self.lastPoint,offset,self.context)
                component.invalidate()

            self.lastPoint = newPoint

            ## Invalidate the new location where the connectors are now
            #for component in self.affectedConnectors:
            #    self.context.invalidateComponent(component)


