from Component import *
from Path import *
from OpenPath import *
from ClosedPath import *
from Rect import *
from Menu import *

# Unlike the Path component (and it's children), this class is aware it part of a GUI.  It handles
# events and whatnot.
class PathComponent(Component):

    def __init__(self,parent,element):
        super().__init__(parent)
        self.element = element
        self.rightClickPoint = None
        self.editing = False
        self.pathElementEditing = None
        self.updateElement(element)

    def updateElement(self,element):

        if element.pathType == PathType.CLOSED:
            self.renderer = ClosedPath(element)
        else:
            self.renderer = OpenPath(element)
            self.renderer.startArrow = element.startArrow
            self.renderer.endArrow = element.endArrow

        self.renderer.corners = element.corners

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
        self.pathElementEditing.edit(offset)

    def showContextMenu(self,point,_):
        self.rightClickPoint = point
        if self.editing:
            options = ["stop editing","split","join"]
        else:
            options = ["edit shape"]
        pathElement = self.renderer.pathElementAt(point)
        if isinstance(pathElement,OpenPath.ArrowElbow):
            options += [ "──", "─>", "─▷" ]
        else:
            options += [ "toggle thickness","toggle style","toggle corners","toggle transparency"]
        self.getDiagramComponent().showMenu(Menu(self,options,point,self.menuResult))

    def menuResult(self,menu):
        selected = menu.getSelectedOption()
        if selected=="split":
            self.split(self.rightClickPoint)
        elif selected=="join":
            self.join(self.rightClickPoint)
        elif selected=="toggle thickness":
            self._setThickness(1-int(self.element.thickness))
        elif selected=="toggle style":
            self._setStyle(1-int(self.element.style))
        elif selected=="toggle corners":
            corners = self.element.corners
            self._setCorners( Corners.SQUARE if corners==Corners.ROUND else Corners.ROUND )
        elif selected=="stop editing":
            self.editing = False
        elif selected=="edit shape":
            self.editing = True
        elif selected=="──":
            self._setArrow(Arrow.NONE)
        elif selected=="─>":
            self._setArrow(Arrow.LINES)
        elif selected=="─▷":
            self._setArrow(Arrow.TRIANGLE)
        elif selected=="toggle transparency":
            corners = self.element.fill
            self._setFill( Fill.TRANSPARENT if corners==Fill.OPAQUE else Fill.OPAQUE )

    def split(self,point):
        pathElement = self.renderer.pathElementAt(point)
        if isinstance(pathElement,Path.Segment):
            if pathElement.orientation==Orientation.HORIZONTAL:
                splitPos = point.x
            else:
                splitPos = point.y
            pathElement.split(splitPos)

    def join(self,point):
        self.invalidate()
        pathElement = self.renderer.pathElementAt(point)
        if pathElement.orientation==Orientation.HORIZONTAL:
            joinPos = point.x
        else:
            joinPos = point.y
        pathElement.join(joinPos)
        self.invalidate()

    def _setThickness(self,thickness):
        self.element.thickness = thickness
        self._updateStroke()

    def _setStyle(self,style):
        self.element.style = style
        self._updateStroke()

    def _setCorners(self,corners):
        self.element.corners = corners
        self._updateStroke()

    def _setFill(self,fill):
        self.element.fill = fill
        self._updateStroke()

    def _updateStroke(self):
        self.renderer.updateStroke()
        self.invalidate()

    def _setArrow(self,arrow):
        print("setting arrow to="+str(arrow))
        pathElement = self.renderer.pathElementAt(self.rightClickPoint)
        element = self.element
        renderer = self.renderer
        if pathElement.index==0:
            element.startArrow = arrow
            renderer.updateArrow(True)
        else:
            element.endArrow = arrow
            renderer.updateArrow(False)
        self.invalidate()

    def __str__(self):
        return "Component{element="+self.element.__str__()+"}";
