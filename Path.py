from Util import *
from Model import *
from Rect import *

class Path:

    _squareCorners  = [ "┌", "┐", "└", "┘" ]
    _roundCorners = [ "╭", "╮", "╰", "╯" ]

    def __init__(self,initialOrientation,elbowRefs):
        self._elbowRefs = elbowRefs
        self.initialOrientation = initialOrientation
        #self.corners = Corners.SQUARE
        self.corners = Corners.ROUND
        self.segments = self.createSegmentList(elbowRefs)

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
        if name=="corners":
            self._setCorners(value)
        super().__setattr__(name,value)

    #def appendElbowReference(self,elbowReference):
    #    self._elbowRefs.append(elbowReference) = segmentIndex+2)

    #def appendElbowValue(self,elbowValue):
    #    self.appendElbowReference(ConstReference(elbowValue))

    class Elbow:

        def __init__(self,xRef,yRef):
            self.xRef = xRef
            self.yRef = yRef

        class Snapshot:
            def __init__(self,x,y,char):
                self.x = x
                self.y = y
                self.char = char

        def x(self):
            return self.xRef.get()

        def y(self):
            return self.yRef.get()

        def point(self):
            return Point(self.x(),self.y())

        def getRect(self):
            return Rect().includePoint(self.point())

        def __str__(self):
            return "Elbow{x="+str(self.xRef.get())+",y="+str(self.yRef.get())+"}"

    def createElbowList(self,refList):
        elbowList = []
        horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
        first = True
        prevDirection = None
        xPrev = None
        yPrev = None
        prevElbow = None
        x=None
        y=None

        for elbowRef in refList:

            if horizontalOrienation:
                xRef = elbowRef
            else:
                yRef = elbowRef

            if first:
                first = False
            else:
                elbow = Path.Elbow(xRef,yRef)
                elbowList.append(elbow)
                prevElbow = elbow
            horizontalOrienation = not horizontalOrienation

        return elbowList

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
                return self.fromElbow.yRef
            else:
                return self.fromElbow.xRef

        def getSnapshot(self,fullLength=False):
            if self.orientation==Orientation.HORIZONTAL:
                fromX = self.fromElbow.x()
                toX = self.toElbow.x()
                minX = min(fromX,toX)
                maxX = max(fromX,toX)
                if not fullLength:
                    minX+=1
                    maxX-=1
                y = self.fromElbow.y()
                return Path.Segment.Snapshot(y,minX,maxX)
            else:
                fromY = self.fromElbow.y()
                toY = self.toElbow.y()
                minY = min(fromY,toY)
                maxY = max(fromY,toY)
                if not fullLength:
                    minY+=1
                    maxY-=1
                x = self.fromElbow.x()
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

            elbowRefs = self.parent._elbowRefs
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
            elbowRefs = self.parent._elbowRefs

            segmentIndex = self.getMySegmentIndex()
            for a in range(3):
                del elbowRefs[(segmentIndex)%len(elbowRefs)]
            elbowRefs.insert((segmentIndex)%len(elbowRefs),VarReference(pos))

            oldSegments = self.parent.segments
            newSegments = self.parent.segments = self.parent.createSegmentList(elbowRefs)

            for listener in self.listeners:
                listener.segmentJoined(oldSegments[segmentIndex-1],oldSegments[segmentIndex],oldSegments[segmentIndex+1],self)


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
        if self.initialOrientation == Orientation.HORIZONTAL:
            xElement = 0
        else:
            xElement = 1

        arrayElement = 0
        for ref in self._elbowRefs:
            if arrayElement%2 == xElement:
                elementOffset = offset.x
            else:
                elementOffset = offset.y
            ref.set( ref.get() + elementOffset )
            arrayElement += 1

    def draw(self,context):
        self.drawSegmentList(context,self.segments)

    def drawSegmentList(self,context,createSegmentList):
        pass  #subclass draws how it sees fit
