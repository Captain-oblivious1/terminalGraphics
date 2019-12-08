from Components import *
from Path import *
from Connector import *
from Util import *

class PathComponent(Component):

    class Segment(Component):

        def __init__(self,parent,pathSegment):
            Component.__init__(self,None)
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
            context.invalidateComponent(self.parent)

            if self.pathSegment.orientation == Orientation.HORIZONTAL:
                myOffset = offset.y
            else:
                myOffset = offset.x

            ref = self.pathSegment.getPosRef()
            oldPos = ref.get()
            ref.set(oldPos+myOffset)

    class Elbow(Component):

        def __init__(self,parent,pathElbow):
            Component.__init__(self,None)
            self.parent = parent
            self.pathElbow = pathElbow

        def draw(self,context):
            pass

        def getRect(self):
            return self.pathElbow.getRect()

        def move(self,offset,context):
            if self.parent.isEditing():
                context.invalidateComponent(self.parent)

                oldPoint = self.pathElbow.point()
                self.pathElbow.xRef.set(oldPoint.x+offset.x)
                self.pathElbow.yRef.set(oldPoint.y+offset.y)

    def __init__(self,pathElement):
        Component.__init__(self,pathElement)
        self.setEditing(True)
        self.createChildren(True)

    def setEditing(self,editing):
        self.editing = editing

    def isEditing(self):
        return self.editing

    def isOnMe(self,point):
        for seg in self.segments:
            if seg.isOnMe(point):
                return True
        return False

    def createChildren(self,closed):
        element = self.element
        self.path = Connector(element.startOrientation)
        #self.path = Path(element.startOrientation,closed)
        for index in range(len(element.turns)):
            self.path.appendElbowReference( ArrayElementReference(element.turns,index) )

        self.segmentList = self.path.createSegmentList()
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
