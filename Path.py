from Util import *
from Model import *
from Rect import *

class Path:

    _squareCorners  = [ "┌", "┐", "└", "┘" ]
    _roundCorners = [ "╭", "╮", "╰", "╯" ]

    def __init__(self,initialOrientation=None,elbowRefs=None):
        self.initialOrientation = initialOrientation
        self.elbowRefs = elbowRefs
        self.corners = Corners.ROUND

    def _setCorners(self,value):
        if value==Corners.SQUARE:
            array = Path._squareCorners
        else:
            array = Path._roundCorners
        setattr(self,"cornerCharArray", array )
        tl = array[0]
        tr = array[1]
        bl = array[2]
        br = array[3]
        self.elbowSymbol = \
              [ [" ","╶","╷","╴","╵"],
                ["╴","─", tr," ", br],  \
                ["╵", bl,"│", br," "],  \
                ["╶"," ", tl,"─", bl],  \
                ["╷", tl," ", tr,"│"] ]

    def __setattr__(self,name,value):
        super().__setattr__(name,value)
        if name=="corners":
            self._setCorners(value)
        elif name=="elbowRefs":
            self.segments = self.createSegmentList(value)

    def createElbow(self,path,index,xRefIndex,yRefIndex):
        return Path.Elbow(path,index,xRefIndex,yRefIndex)

    def getRect(self):
        rect = Rect()
        for segment in self.segments:
            rect.unionWith(segment.getRect())
        return rect

    def createElbowList(self,refList):
        elbowList = []
        horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
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
        horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
        for elbow in elbows:
            if prevElbow:
                segment = Path.Segment(self)
                segment.fromElbow = prevElbow
                segment.toElbow = elbow
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
        #print("Path.move offset x="+str(offset.x)+" y="+str(offset.y))
        if self.initialOrientation == Orientation.HORIZONTAL:
            xElement = 0
        else:
            xElement = 1

        arrayElement = 0
        for ref in self.elbowRefs:
            if arrayElement%2 == xElement:
                elementOffset = offset.x
            else:
                elementOffset = offset.y
            ref.set( ref.get() + elementOffset )
            arrayElement += 1

    def isPointInPath(self,point):
        return self.pathElementAt(point)!=None

    def pathElementAt(self,point):
        for segment in self.segments:
            fromElbow = segment.fromElbow
            if point.isEqual(fromElbow.getX(), fromElbow.getY()):
                return fromElbow
            elif segment.getRect().isInsidePoint(point):
                return segment
        return None

    #def draw(self,context):
    #    self.drawSegmentList(context,self.segments)

    #def drawSegmentList(self,context,createSegmentList):
    #    pass  #subclass draws how it sees fit

    class Elbow:

        def __init__(self,path,index,xRefIndex,yRefIndex):
            self.path = path
            self.index = index
            self.xRefIndex = xRefIndex
            self.yRefIndex = yRefIndex

        class Snapshot:
            def __init__(self,x,y,char):
                self.x = x
                self.y = y
                self.char = char

        def _allElbowRefs(self):
            return self.path.elbowRefs

        def getXRef(self):
            return self._allElbowRefs()[self.xRefIndex]

        def getX(self):
            return self.getXRef().get()

        def setX(self,value):
            return self.getXRef().set(value)

        def getYRef(self):
            return self._allElbowRefs()[self.yRefIndex]

        def getY(self):
            return self.getYRef().get()

        def setY(self,value):
            return self.getYRef().set(value)

        def point(self):
            return Point(self.getX(),self.getY())

        def getRect(self):
            return Rect().includePoint(self.point())

        def __str__(self):
            return "Elbow{index="+str(self.index)+" x="+str(self.getX())+",y="+str(self.getY())+"}"

    class Segment:
        def __init__(self,parent):
            self.parent = parent
            self.fromElbow = None
            self.toElbow = None
            self.orientation = None
            self.listeners = set({})

        class Snapshot:
            def __init__(self,pos,fro,to):
                self.pos = pos
                self.fro = fro
                self.to = to

        def getPosRef(self):
            if self.orientation==Orientation.HORIZONTAL:
                return self.parent.elbowRefs[self.fromElbow.yRefIndex]
            else:
                return self.parent.elbowRefs[self.fromElbow.xRefIndex]

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

        def addListener(self,listener):
            self.listeners.add(listener)

        def removeListener(self,listener):
            self.listeners.remove(listener)

 
        def split(self,pos):
            segmentIndex = self.getMySegmentIndex()

            elbowRefs = self.parent.elbowRefs
            currentElbowRefLen = len(elbowRefs)
            splitIndex = (segmentIndex+1)%currentElbowRefLen
            insertIndex = (segmentIndex+2)%currentElbowRefLen
            elbowRefs.insert(insertIndex,VarReference(elbowRefs[splitIndex].get()))
            elbowRefs.insert(insertIndex,VarReference(pos))

            oldSegments = self.parent.segments
            newSegments = self.parent.segments = self.parent.createSegmentList(elbowRefs)

            for index in range(segmentIndex):
                newSegments[index].listeners = oldSegments[index].listeners

            for index in range(segmentIndex+1,len(oldSegments)):
                newSegments[index+2].listeners = oldSegments[index].listeners

            for listener in self.listeners:
                listener.segmentSplit(self,newSegments[segmentIndex],newSegments[segmentIndex+1],newSegments[segmentIndex+2])

        def join(self,pos):
            elbowRefs = self.parent.elbowRefs

            segmentIndex = self.getMySegmentIndex()
            for _ in range(3):
                del elbowRefs[(segmentIndex)%len(elbowRefs)]
            elbowRefs.insert((segmentIndex)%len(elbowRefs),VarReference(pos))

            oldSegments = self.parent.segments
            newSegments = self.parent.segments = self.parent.createSegmentList(elbowRefs)

            for listener in self.listeners:
                listener.segmentJoined(oldSegments[segmentIndex-1],oldSegments[segmentIndex],oldSegments[segmentIndex+1],self)

