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
        self.updateElement(element)

    def updateElement(self,element):
        refArray = []
        for val in element.turns:
           refArray.append( VarReference(val) )

        if element.pathType == PathType.CLOSED:
            self.renderer = ClosedPath(element.startOrientation,refArray,element.fill == Fill.OPAQUE)
        else:
            self.renderer = OpenPath(element.startOrientation,refArray)
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

    def move(self,fromPoint,offset,context):
        if self.editing:
            self.editShape(fromPoint,offset,context)
        else:
            self.renderer.move(offset,context)

    def editShape(self,fromPoint,offset,context):
        self.invalidate()

        pathElement = self.renderer.pathElementAt(fromPoint)
        if pathElement==None:
            print("Warning pathElement was None for some reason")
        else: # is elbow
            pathElement.edit(offset)

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
        self.parent.invalidate()
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

#    def createChildren(self):
#        self.createChildrenRenderer(self.renderer)
#
#    def createChildrenRenderer(self,path):
#        element = self.element
#        self.path = path
#
#        self.segmentList = self.path.getSegmentList()
#        self.segments = []
#        for pathSegment in self.segmentList:
#            self.segments.append( PathComponent.Segment( self, pathSegment ) )
#
#        self.elbows = []
#        prevSegment = None
#        for segment in self.segments:
#            self.elbows.append(PathComponent.Elbow(self,segment.pathSegment.fromElbow))
#            prevSegment = segment
#        self.elbows.append(PathComponent.Elbow(self,prevSegment.pathSegment.toElbow))



#    def children(self):
#        returnMe = set()
#        if True or self.isEditing():
#            for segment in self.segments:
#                returnMe.add(segment)
#            for elbow in self.elbows:
#                returnMe.add(elbow)
#        return returnMe

    #def setSelected(self,selected):
    #    Component.setSelected(self,selected)
    #    #for seg in self.segments:
    #    #    seg.setSelected(selected)


#    class Segment(Component):
#
#        def __init__(self,parent,pathSegment):
#            super().__init__(parent)
#            self.pathSegment = pathSegment
#            self.parent = parent
#
#        #def draw(self,context):
#        #    pass
#
#        def setSelected(self,newSelected):
#            self.parent.setSelected(newSelected)
#
#        def isSelected(self):
#            return self.parent.isSelected()
#
#        def getRect(self):
#            return self.pathSegment.getRect()
#
#        def move(self,offset,context):
#            if self.parent.isEditing():
#                self.forceMove(offset,context)
#            #else:
#                #self.parent.invalidate()
#                #self.parent.move(offset,context)
#                #self.parent.invalidate()
#                
#
#        def forceMove(self,offset,context):
#            self.parent.invalidate()
#
#            if self.pathSegment.orientation == Orientation.HORIZONTAL:
#                myOffset = offset.y
#            else:
#                myOffset = offset.x
#
#            ref = self.pathSegment.getPosRef()
#            oldPos = ref.get()
#            ref.set(oldPos+myOffset)
#
#        def split(self,point):
#            pathSegment = self.pathSegment
#            if pathSegment.orientation==Orientation.HORIZONTAL:
#                splitPos = point.x
#            else:
#                splitPos = point.y
#            pathSegment.split(splitPos)
#            self.parent.createChildren()
#
#        def join(self,point):
#            self.parent.invalidate()
#            pathSegment = self.pathSegment
#            if pathSegment.orientation==Orientation.HORIZONTAL:
#                joinPos = point.x
#            else:
#                joinPos = point.y
#            pathSegment.join(joinPos)
#            self.parent.createChildren()
#            self.parent.invalidate()
#
#        def showContextMenu(self,point,context):
#            if self.parent.isEditing():
#                options = ["stop editing","","split","join"]
#            else:
#                options = ["edit shape"]
#            self.getTopLevelComponent().showMenu(Menu(self,options,point,self.menuResult))
#
#        def menuResult(self,menu):
#            if menu.getSelectedOption()=="split":
#                self.split(menu.getTopLeft())
#            elif menu.getSelectedOption()=="join":
#                self.join(menu.getTopLeft())
#            elif menu.getSelectedOption()=="stop editing":
#                self.parent.setEditing(False)
#            elif menu.getSelectedOption()=="edit shape":
#                self.parent.setEditing(True)
#
#    class ComponentSelectListener:
#        def __init__(self,elbow):
#            self.elbow = elbow
#
#        def componentSelected(self,component,point):
#            if isinstance(component,PathComponent.Segment):
#                self.elbow.parent.invalidate()
#                pathSegment = component.pathSegment
#                self.elbow.pathElbow.connectTo(pathSegment,point)
#                self.elbow.parent.invalidate()
#                self.elbow.getEditor().goIdleState()
#
#    class Elbow(Component):
#
#        def __init__(self,parent,pathElbow):
#            super().__init__(parent)
#            self.pathElbow = pathElbow
#
#        def setSelected(self,newSelected):
#            self.parent.setSelected(newSelected)
#
#        def isSelected(self):
#            return self.parent.isSelected()
#
#        #def draw(self,context):
#        #    pass
#
#        def getRect(self):
#            return self.pathElbow.getRect()
#
#        def move(self,offset,context):
#            if self.parent.isEditing():
#                self.parent.invalidate()
#
#                oldPoint = self.pathElbow.point()
#                self.pathElbow.setX(oldPoint.x+offset.x)
#                self.pathElbow.setY(oldPoint.y+offset.y)
#            else:
#                #self.parent.invalidate()
#                #self.parent.move(offset,context)
#                #self.parent.invalidate()
#                self.invalidate()
#                Component.move(self,offset,text)
#
#
#        def showContextMenu(self,point,context):
#            if "connectTo" in dir(self.pathElbow):
#                options = ["Connect to"]
#                self.getTopLevelComponent().showMenu(Menu(self,options,point,self.menuResult))
#
#        def menuResult(self,menu):
#            if menu.getSelectedOption()=="Connect to":
#                editor = self.getEditor()
#                editor.goSelectComponentState(PathComponent.ComponentSelectListener(self))
#                #self.pathElbow.connectTo()
