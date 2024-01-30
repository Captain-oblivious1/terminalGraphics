from Util import *
from Model import *
from Rect import *

# This class has no idea it's part of any GUI.  It knows nothing about Editor, Events, Components,
# and whatnot.  It only know of the element object and the Context it uses to draw.
class Path:

    _squareCorners  = [ [ "┌", "┐", "└", "┘" ],
                        [ "┏", "┓", "┗", "┛" ] ]
    _roundCorners = [ "╭", "╮", "╰", "╯" ]

    _horizontalLines = [ ['─', '╌'],
                         ['━', '╍'] ]

    _verticalLines = [ ['│', '╎'],
                       ['┃', '╏'] ]

    _halfLines = [ [ "╴", "╶", "╵", "╷" ],
                   [ "╸", "╺", "╹", "╻" ] ]

    def __init__(self,element):
        self.element = element
        self.updateStroke()
        self.updateShape()

    def updateStroke(self):
        thickInt = int(self.element.thickness)
        styleInt = int(self.element.style)
        halfLineArray = Path._halfLines[thickInt]
        if self.element.corners==Corners.SQUARE:
            cornerArray = Path._squareCorners[thickInt]
        else:
            cornerArray = Path._roundCorners
        setattr(self,"cornerCharArray", cornerArray )
        tl = cornerArray[0]
        tr = cornerArray[1]
        bl = cornerArray[2]
        br = cornerArray[3]
        l = halfLineArray[0]
        r = halfLineArray[1]
        t = halfLineArray[2]
        b = halfLineArray[3]
        h = Path._horizontalLines[thickInt][styleInt]
        v = Path._verticalLines[thickInt][styleInt]
        s = ' '
        self.elbowSymbol = \
              [ [  s,  r,  b,  l,  t],
                [  l,  h, tr,  s, br],  \
                [  t, bl,  v, br,  s],  \
                [  r,  s, tl,  h, bl],  \
                [  b, tl,  s, tr,  v] ]

    def updateShape(self):
        self.segments = self.createSegmentList(self.element.turns)

    def createElbow(self,path,index,xRefIndex,yRefIndex):
        return Path.Elbow(self,path,index,xRefIndex,yRefIndex)

    def getRect(self):
        rect = Rect()
        for segment in self.segments:
            rect.unionWith(segment.getRect())
        return rect

    def createElbowList(self,refList):
        elbowList = []
        horizontalOrienation = self.element.startOrientation==Orientation.HORIZONTAL
        first = True

        elbowIndex = 0
        refIndex = 0
        for refIndex in range(len(refList)):

            if horizontalOrienation:
                xRefIndex = refIndex
            else:
                yRefIndex = refIndex

            refIndex += 1

            if first:
                first = False
            else:
                elbow = self.createElbow(self,elbowIndex,xRefIndex,yRefIndex)
                elbowIndex += 1
                elbowList.append(elbow)
            horizontalOrienation = not horizontalOrienation

        return elbowList

    def createSegmentList(self,elbowRefs):
        elbows = self.createElbowList(elbowRefs)
        segmentList = []
        prevElbow = None
        horizontalOrienation = self.element.startOrientation==Orientation.HORIZONTAL
        for elbow in elbows:
            if prevElbow:
                segment = Path.Segment(self)
                segment.fromElbow = prevElbow
                prevElbow.toSegment = segment
                segment.toElbow = elbow
                elbow.fromSegment = segment
                if horizontalOrienation:
                    segment.orientation = Orientation.HORIZONTAL
                else:
                    segment.orientation = Orientation.VERTICAL

                horizontalOrienation = not horizontalOrienation

                segmentList.append( segment )

            prevElbow = elbow

        return segmentList

    def getSegmentList(self):
        return self.segments

    def move(self,offset,context):
        element = self.element
        if element.startOrientation == Orientation.HORIZONTAL:
            xElement = 0
        else:
            xElement = 1

        arrayElement = 0
        for ref in element.turns:
            if arrayElement%2 == xElement:
                elementOffset = offset.x
            else:
                elementOffset = offset.y
            element.turns[arrayElement] = ref + elementOffset
            arrayElement += 1

    def isPointInPath(self,point):
        return self.pathElementAt(point)!=None

    def pathElementAt(self,point):
        for segment in self.segments:
            fromElbow = segment.fromElbow
            if fromElbow.isAtPoint(point):
                return fromElbow
            elif segment.getRect().isInsidePoint(point):
                return segment

        lastElbow = self.segments[-1].toElbow
        if lastElbow.isAtPoint(point):
            return lastElbow
        else:
            return None

    class Elbow:

        def __init__(self,parent,path,index,xRefIndex,yRefIndex):
            self.parent = parent
            self.path = path
            self.index = index
            self.xRefIndex = xRefIndex
            self.yRefIndex = yRefIndex
            self.fromSegment = None
            self.toSegment = None

        class Snapshot:
            def __init__(self,x,y,char):
                self.x = x
                self.y = y
                self.char = char

        def _allElbowRefs(self):
            return self.path.elbowRefs

        def getX(self):
            turns = self.parent.element.turns
            return turns[self.xRefIndex % len(turns)]

        def setX(self,value):
            self.parent.element.turns[self.xRefIndex] = value

        def getY(self):
            turns = self.parent.element.turns
            return turns[self.yRefIndex % len(turns)]

        def setY(self,value):
            self.parent.element.turns[self.yRefIndex] = value

        def point(self):
            return Point(self.getX(),self.getY())

        def getRect(self):
            return Rect().includePoint(self.point())

        def isAtPoint(self,point):
            return point==Point(self.getX(), self.getY())

        def edit(self,offset):
            if self.fromSegment!=None:
                self.fromSegment.edit(offset)
            if self.toSegment!=None:
                self.toSegment.edit(offset)

        def __str__(self):
            return "Elbow{index="+str(self.index)+" x="+str(self.getX())+",y="+str(self.getY())+"}"

    class Segment:
        def __init__(self,parent):
            self.parent = parent
            self.fromElbow = None
            self.toElbow = None
            self.orientation = None

        class Snapshot:
            def __init__(self,pos,fro,to):
                self.pos = pos
                self.fro = fro
                self.to = to

        def getPosIndex(self):
            if self.orientation==Orientation.HORIZONTAL:
                index = self.fromElbow.yRefIndex
            else:
                index = self.fromElbow.xRefIndex
            return index % len(self.parent.element.turns)

        def getSnapshot(self,fullLength=False):
            if self.orientation==Orientation.HORIZONTAL:
                fromX = self.fromElbow.getX()
                toX = self.toElbow.getX()
                minX = min(fromX,toX)
                maxX = max(fromX,toX)
                if not fullLength:
                    minX+=1
                    maxX-=1
                y = self.fromElbow.getY()
                return Path.Segment.Snapshot(y,minX,maxX)
            else:
                fromY = self.fromElbow.getY()
                toY = self.toElbow.getY()
                minY = min(fromY,toY)
                maxY = max(fromY,toY)
                if not fullLength:
                    minY+=1
                    maxY-=1
                x = self.fromElbow.getX()
                return Path.Segment.Snapshot(x,minY,maxY)

        def getRect(self):
            snapshot = self.getSnapshot()
            if self.orientation==Orientation.HORIZONTAL:
                return Rect(snapshot.fro,snapshot.pos,snapshot.to-snapshot.fro+1,1)
            else:
                return Rect(snapshot.pos,snapshot.fro,1,snapshot.to-snapshot.fro+1)

        def direction(self):
            return vectorToDirection(self.toElbow.point()-self.fromElbow.point())

        def getMySegmentIndex(self):
            segmentIndex = 0
            for segment in self.parent.segments:
                if segment == self:
                    break
                segmentIndex+=1
            return segmentIndex

        def edit(self,offset):
            if self.orientation == Orientation.HORIZONTAL:
                myOffset = offset.y
            else:
                myOffset = offset.x
            index = self.getPosIndex()
            self.parent.element.turns[index] += myOffset

        def split(self,pos):
            segmentIndex = self.getMySegmentIndex()

            turns = self.parent.element.turns
            currentElbowRefLen = len(turns)
            splitIndex = (segmentIndex+1)%currentElbowRefLen
            insertIndex = (segmentIndex+2)%currentElbowRefLen
            turns.insert(insertIndex,turns[splitIndex])
            turns.insert(insertIndex,pos)
            self.parent.updateShape()

        def join(self,pos):
            turns = self.parent.element.turns
            segmentIndex = self.getMySegmentIndex()
            for _ in range(3):
                del turns[(segmentIndex)%len(turns)]
            turns.insert((segmentIndex)%len(turns),pos)
            self.parent.updateShape()
