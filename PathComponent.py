from Component import *
from Path import *
#from Connector import *
#from Shape import *
from Util import *
from Rect import *
from Menu import *

class PathComponent(Component):

    class Segment(Component):

        def __init__(self,parent,pathSegment):
            super().__init__(parent)
            self.pathSegment = pathSegment
            self.parent = parent

        def draw(self,context):
            pass

        def getRect(self):
            return self.pathSegment.getRect()

        def move(self,offset,context):
            if self.parent.isEditing():
                self.forceMove(offset,context)

        def forceMove(self,offset,context):
            self.parent.invalidate()

            if self.pathSegment.orientation == Orientation.HORIZONTAL:
                myOffset = offset.y
            else:
                myOffset = offset.x

            ref = self.pathSegment.getPosRef()
            oldPos = ref.get()
            ref.set(oldPos+myOffset)

        def split(self,point):
            pathSegment = self.pathSegment
            if pathSegment.orientation==Orientation.HORIZONTAL:
                splitPos = point.x
            else:
                splitPos = point.y
            pathSegment.split(splitPos)
            self.parent.createChildren()

        def join(self,point):
            self.parent.invalidate()
            pathSegment = self.pathSegment
            if pathSegment.orientation==Orientation.HORIZONTAL:
                joinPos = point.x
            else:
                joinPos = point.y
            pathSegment.join(joinPos)
            self.parent.createChildren()
            self.parent.invalidate()

        def showContextMenu(self,point,context):
            self.getTopLevelComponent().showMenu(Menu(self,["split","join"],point,self.menuResult))

        def menuResult(self,menu):
            if menu.getSelectedOption()=="split":
                self.split(menu.getTopLeft())
            elif menu.getSelectedOption()=="join":
                self.join(menu.getTopLeft())


    class Elbow(Component):

        def __init__(self,parent,pathElbow):
            super().__init__(parent)
            self.pathElbow = pathElbow

        def draw(self,context):
            pass

        def getRect(self):
            return self.pathElbow.getRect()

        def move(self,offset,context):
            if self.parent.isEditing():
                self.parent.invalidate()

                oldPoint = self.pathElbow.point()
                self.pathElbow.xRef.set(oldPoint.x+offset.x)
                self.pathElbow.yRef.set(oldPoint.y+offset.y)

    def __init__(self,parent,element,renderer):
        super().__init__(parent)
        self.element = element
        self.renderer = renderer
        self.setEditing(True)
        self.createChildren()

    def setEditing(self,editing):
        self.editing = editing

    def isEditing(self):
        return self.editing

    def isOnMe(self,point):
        for seg in self.segments:
            if seg.isOnMe(point):
                return True
        return False

    def createChildren(self):
        self.createChildrenRenderer(self.renderer)

    def createChildrenRenderer(self,path):
        element = self.element
        self.path = path
        #self.path = Connector(element.startOrientation)
        #self.path = Shape(element.startOrientation)
        #refArray = []
        #for index in range(len(element.turns)):
        #    refArray.append(ArrayElementReference(element.turns,index))

        self.segmentList = self.path.getSegmentList()
        self.segments = []
        for pathSegment in self.segmentList:
            self.segments.append( PathComponent.Segment( self, pathSegment ) )

        self.elbows = []
        prevSegment = None
        for segment in self.segments:
            self.elbows.append(PathComponent.Elbow(self,segment.pathSegment.fromElbow))
            prevSegment = segment
        self.elbows.append(PathComponent.Elbow(self,prevSegment.pathSegment.toElbow))


    def getRect(self):
        rect = Rect()
        for seg in self.segments:
            rect.unionWith(seg.getRect())
        rect.unionWith(self.elbows[0].getRect())
        rect.unionWith(self.elbows[-1].getRect())
        return rect

    def draw(self,context):
        self.path.drawSegmentList(context,self.segmentList)

    def children(self):
        returnMe = set()
        if self.isEditing():
            for segment in self.segments:
                returnMe.add(segment)
            for elbow in self.elbows:
                returnMe.add(elbow)
        return returnMe

    def setSelected(self,selected):
        Component.setSelected(self,selected)
        for seg in self.segments:
            seg.setSelected(selected)

    def move(self,offset,context):
        self.path.move(offset,context)
