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

        #def getFullRect(self):
        #    pos = self.posRef.get()
        #    rawFrom = self.fromRef.get()
        #    rawTo = self.toRef.get()
        #    fro = min(rawFrom,rawTo)
        #    to = max(rawFrom,rawTo)
        #    if to-fro<=1:
        #        return Rect()
        #    elif self.orientation == Orientation.HORIZONTAL:
        #        return Rect(fro,pos,to-fro+1,1)
        #    else:
        #        return Rect(pos,fro,1,to-fro+1)

        def move(self,offset,context):
            if self.parent.isEditing():
                self.forceMove(offset,context)

        def forceMove(self,offset,context):
            rect = self.getFullRect()
            context.invalidateRect(rect)

            if self.orientation == Orientation.HORIZONTAL:
                myOffset = offset.y
            else:
                myOffset = offset.x

            ref = self.pathSegment.getPosRef()
            oldPos = ref.get()
            ref.set(oldPos+myOffset)

    #class Elbow(Component):

    #    #turnSymbol = \
    #    #      [ ["─","╮"," ","╯"], \
    #    #        ["╰","│","╯"," "], \
    #    #        [" ","╭","─","╰"], \
    #    #        ["╭"," ","╮","│"] ]

    #    turnSymbol = \
    #          [ ["─","┐"," ","┘"], \
    #            ["└","│","┘"," "], \
    #            [" ","┌","─","└"], \
    #            ["┌"," ","┐","│"] ]

    #    def __init__(self,beforeSegment,afterSegment):
    #        Component.__init__(self,None)
    #        self.beforeSegment = beforeSegment
    #        self.afterSegment = afterSegment

    #    def getPoint(self):

    #        beforePos = self.beforeSegment.posRef.get()
    #        afterPos = self.afterSegment.posRef.get()

    #        if self.beforeSegment.orientation==Orientation.VERTICAL:
    #            x = beforePos
    #        else:
    #            y = beforePos

    #        if self.afterSegment.orientation==Orientation.VERTICAL:
    #            x = afterPos
    #        else:
    #            y = afterPos

    #        return Point(x,y)

    #    def getInfo(self):
    #        point = self.getPoint()

    #        beforeSum = self.beforeSegment.fromRef.get() + self.beforeSegment.toRef.get()
    #        afterSum = self.afterSegment.fromRef.get() + self.afterSegment.toRef.get()

    #        if self.beforeSegment.orientation==Orientation.VERTICAL:
    #            if beforeSum < 2*point.y:
    #                beforeDirection = Direction.DOWN
    #            elif beforeSum > 2*point.y:
    #                beforeDirection = Direction.UP
    #            else:
    #                beforeDirection = Direction.RIGHT if beforeSum<afterSum else Direction.LEFT
    #        else:
    #            if beforeSum < 2*point.x:
    #                beforeDirection = Direction.RIGHT
    #            elif beforeSum > 2*point.x:
    #                beforeDirection = Direction.LEFT
    #            else:
    #                beforeDirection = Direction.DOWN if beforeSum<afterSum else Direction.UP

    #        if self.afterSegment.orientation==Orientation.VERTICAL:
    #            if afterSum < 2*point.y:
    #                afterDirection = Direction.UP
    #            elif afterSum > 2*point.y:
    #                afterDirection = Direction.DOWN
    #            else:
    #                afterDirection = Direction.RIGHT if beforeSum<afterSum else Direction.LEFT
    #        else:
    #            if afterSum < 2*point.x:
    #                afterDirection = Direction.LEFT
    #            elif afterSum > 2*point.x:
    #                afterDirection = Direction.RIGHT
    #            else:
    #                afterDirection = Direction.DOWN if beforeSum<afterSum else Direction.UP

    #        return point,PathComponent.Elbow.turnSymbol[beforeDirection.value][afterDirection.value]

    #    def getRect(self):
    #        return Rect().includePoint( self.getPoint() )

    #    def draw(self,context):
    #        point,char = self.getInfo()
    #        context.orChar(point.x,point.y,char,self.selected)

    #    def move(self,offset,context):
    #        self.beforeSegment.move(offset,context)
    #        self.afterSegment.move(offset,context)


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
        path = Path(element.startOrientation)
        for index in range(len(element.turns)):
            path.appendTurnRef( ArrayElementReference(element.turns,index) )

        self.segments = []
        for pathSegment in path.createSegmentList():
            self.segments.append( PathComponent.Segment( self, pathSegment ) )


        #self.segments = []
        #self.elbows = []

        #self.refs = []
        #refs = self.refs

        #horizontalOrientation = element.startOrientation==Orientation.HORIZONTAL

        #if horizontalOrientation:
        #    refs.append( AttrReference(element.startPoint,"x") )
        #    refs.append( AttrReference(element.startPoint,"y") )
        #else:
        #    refs.append( AttrReference(element.startPoint,"y") )
        #    refs.append( AttrReference(element.startPoint,"x") )

        #for index in range(len(element.turns)):
        #    refs.append( ArrayElementReference(element.turns,index) )

        #self.createSegments(refs,horizontalOrientation)
        #self.createElbows(refs)

    def createSegments(self,refs,startHorizontal):
        directionMap = { True:Orientation.HORIZONTAL, False:Orientation.VERTICAL }
        for index in range(len(refs)-2):
            self.segments.append( PathComponent.Segment(self,refs[index],refs[index+1],refs[index+2],directionMap[startHorizontal]) )
            startHorizontal = 1 - startHorizontal

    def createElbows(self,refs):
        prevSegment = None
        for segment in self.segments:
            if prevSegment:
                self.elbows.append( PathComponent.Elbow(prevSegment,segment) )
            prevSegment = segment

    def getRect(self):
        rect = Rect()
        for seg in self.segments:
            rect.unionWith(seg.getRect())
        return rect

    def draw(self,context):

        #turnSymbol = \
        #      [ ["─","╮"," ","╯"], \
        #        ["╰","│","╯"," "], \
        #        [" ","╭","─","╰"], \
        #        ["╭"," ","╮","│"] ]

        turns = [80,5,85,30,75,23]
        path = Path(Orientation.HORIZONTAL)
        path.setCorners ( [ "╭", "╮", "╰", "╯", "─", "│" ] )
        for element in range(len(turns)):
            path.appendTurnRef(ArrayElementReference(turns,element))
        path.draw(context)

    #def draw(self,context):
    #    for seg in self.segments:
    #        seg.draw(context)
    #    for elbow in self.elbows:
    #        elbow.draw(context)

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

