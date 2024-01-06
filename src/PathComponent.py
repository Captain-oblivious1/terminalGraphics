from Component import *
from Path import *
from OpenPath import *
from ClosedPath import *
#from Connector import *
#from Shape import *
from Util import *
from Rect import *
from Menu import *

class PathComponent(Component):

    def __init__(self,parent,element):
        super().__init__(parent)
        self.element = element
        self.rightClickPoint = None
        self.editing = False
        self.pathElementEditing = None
        self.updateElement(element)

    def updateElement(self,element):

        turnArrayReference = AttrReference(element,"turns")

        if element.pathType == PathType.CLOSED:
            self.renderer = ClosedPath(element.startOrientation,turnArrayReference,element.fill == Fill.OPAQUE)
        else:
            self.renderer = OpenPath(element.startOrientation,turnArrayReference)
            self.renderer.startArrow = element.startArrow
            self.renderer.endArrow = element.endArrow

        self.renderer.corners = element.corners

    #def setEditing(self,editing):
    #    self.editing = editing

    #def isEditing(self):
    #    return self.editingPoint!=None

    def isOnMe(self,point):
        return self.renderer.isPointInPath(point)

    def getRect(self):
        return self.renderer.getRect()

    def draw(self,context):
        self.renderer.draw(context,self.isSelected())

    def startMove(self,point,context):
        if self.editing:
            self.pathElementEditing = self.renderer.pathElementAt(point)

    def move(self,fromPoint,offset,context):
        if self.editing:
            self.editShape(fromPoint,offset,context)
        else:
            self.renderer.move(offset,context)

    def finishMove(self,point,context):
        if self.editing:
            self.pathElementEditing = None

    def editShape(self,fromPoint,offset,context):
        self.invalidate()

        #pathElement = self.renderer.pathElementAt(fromPoint)
        #if pathElement==None:
        #    print("Warning pathElement was None for some reason")
        #else: # is elbow
        #    pathElement.edit(offset)
        self.pathElementEditing.edit(offset)

    def showContextMenu(self,point,context):
        self.rightClickPoint = point
        if self.editing:
            options = ["stop editing","","split","join"]
        else:
            options = ["edit shape"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        if menu.getSelectedOption()=="split":
            self.split(self.rightClickPoint)
        elif menu.getSelectedOption()=="join":
            self.join(self.rightClickPoint)
        elif menu.getSelectedOption()=="stop editing":
            self.editing = False
        elif menu.getSelectedOption()=="edit shape":
            self.editing = True

    def split(self,point):
        pathElement = self.renderer.pathElementAt(point)
        if isinstance(pathElement,Path.Segment):
            if pathElement.orientation==Orientation.HORIZONTAL:
                splitPos = point.x
            else:
                splitPos = point.y
            pathElement.split(splitPos)
        #self.createChildren()

    def join(self,point):
        #self.parent.invalidate()
        self.invalidate()
        pathElement = self.renderer.pathElementAt(point)
        if pathElement.orientation==Orientation.HORIZONTAL:
            joinPos = point.x
        else:
            joinPos = point.y
        pathElement.join(joinPos)
        #self.parent.createChildren()
        self.invalidate()

    def __str__(self):
        return "Component{element="+self.element.__str__()+"}";
