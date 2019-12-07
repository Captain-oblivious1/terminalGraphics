from Components import *
from Path import *
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
                context.invalidateComponent(self.parent)

                if self.pathSegment.orientation == Orientation.HORIZONTAL:
                    myOffset = offset.y
                else:
                    myOffset = offset.x

                ref = self.pathSegment.getPosRef()
                oldPos = ref.get()
                ref.set(oldPos+myOffset)

    class Elbow(Component):

        #def __init__(self,beforeSegment,afterSegment,pathElbow):
        def __init__(self,parent,pathElbow):
            Component.__init__(self,None)
            #self.beforeSegment = beforeSegment
            #self.afterSegment = afterSegment
            self.parent = parent
            self.pathElbow = pathElbow

        def draw(self,context):
            pass

        def getRect(self):
            #toElbow = self.beforeSegment.pathSegment.toElbow
            #return Rect().includePoint( Point(toElbow.x(),toElbow.y()) )
            return self.pathElbow.getRect()

        def move(self,offset,context):
            if self.parent.isEditing():
                context.invalidateComponent(self.parent)

                oldPoint = self.pathElbow.point()
                self.pathElbow.xRef.set(oldPoint.x+offset.x)
                self.pathElbow.yRef.set(oldPoint.y+offset.y)


            #if self.beforeSegment:
            #    self.beforeSegment.move(offset,context)
            #if self.afterSegment:
            #    self.afterSegment.move(offset,context)


    def __init__(self,pathElement):
        Component.__init__(self,pathElement)
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
        element = self.element
        self.path = Path(element.startOrientation)
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
        element = self.element
        if element.startOrientation == Orientation.HORIZONTAL:
            xElement = 0
        else:
            xElement = 1

        arrayElement = 0
        for ref in self.refs:
            if arrayElement%2 == xElement:
                elementOffset = offset.x
            else:
                elementOffset = offset.y
            ref.set( ref.get() + elementOffset )
            arrayElement += 1

