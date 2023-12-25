#from State import *
#from Util import *
#
#class SelectComponentState(State):
#    def __init__(self,diagramComponent,eventListener):
#        super().__init__()
#        self.diagramComponent = diagramComponent
#        self.selectedComponent = None
#        self.eventListener = eventListener
#
#    def mousePressed(self, x, y):
#        point = Point(x,y)
#        clickedOn = self.diagramComponent.componentAt(point)
#        self.selectedComponent = clickedOn
#
#    def mouseReleased(self, x, y):
#        point = Point(x,y)
#        clickedOn = self.diagramComponent.componentAt(point)
#        if clickedOn != self.selectedComponent:
#            clickedOn = None
#        self.eventListener.componentSelected(clickedOn,point)
