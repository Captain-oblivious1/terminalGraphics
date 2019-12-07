from Util import *
from Model import *
from Components import *

class Path:

    _squareCorners  = [ "┌", "┐", "└", "┘" ]
    _roundCorners = [ "╭", "╮", "╰", "╯" ]

    _noneArrowArray =     [ "╶", "╴", "╷", "╵" ]
    _linesArrowArray =    [ "<", ">", "∧", "∨" ]
    _triangleArrowArray = [ "◁", "▷", "△", "▽" ]

    def __init__(self,initialOrientation):
        self._elbowRefs = []
        self.initialOrientation = initialOrientation
        self.startArrow = Arrow.LINES
        self.endArrow = Arrow.LINES
        self.corners = Corners.ROUNDED

    def _setArrow(self,name,value):
        if value==Arrow.NONE:
            array = Path._noneArrowArray
        elif value==Arrow.LINES:
            array = Path._linesArrowArray
        elif value==Arrow.TRIANGLE:
            array = Path._triangleArrowArray
        setattr(self,name+"CharArray", array)

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
        h =  "─"
        v =  "│"
        self.elbowSymbol = \
              [ [" ","╶","╷","╴","╵"],
                ["╴","─", tr," ", br],  \
                ["╵", bl,"│", br," "],  \
                ["╶"," ", tl,"─", bl],  \
                ["╷", tl," ", tr,"│"] ]

    def __setattr__(self,name,value):
        if name=="startArrow" or name=="endArrow":
            self._setArrow(name,value)
        elif name=="corners":
            self._setCorners(value)
        super().__setattr__(name,value)

    def appendElbowReference(self,elbowReference):
        self._elbowRefs.append(elbowReference)

    class Elbow:

        def __init__(self,xRef,yRef):
            self.xRef = xRef
            self.yRef = yRef
            #self.char = "#"

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
            #return "Elbow{x="+str(self.xRef.get())+",y="+str(self.yRef.get())+",char='"+self.char+"'}"
            return "Elbow{x="+str(self.xRef.get())+",y="+str(self.yRef.get())+"}"

    def createElbowList(self):
        elbowList = []
        horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
        first = True
        prevDirection = None
        xPrev = None
        yPrev = None
        prevElbow = None
        x=None
        y=None
        for elbowRef in self._elbowRefs:

            if horizontalOrienation:
                xRef = elbowRef
                #x = xRef.get()
            else:
                yRef = elbowRef
                #y = yRef.get()

            if first:
                first = False
            else:
                elbow = Path.Elbow(xRef,yRef)
                elbowList.append(elbow)
                prevElbow = elbow
            horizontalOrienation = not horizontalOrienation

        return elbowList

    class Segment:
        def __init__(self):
            self.fromElbow = None
            self.toElbow = None
            self.orientation = None

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

        def getSnapshot(self):
            if self.orientation==Orientation.HORIZONTAL:
                fromX = self.fromElbow.x()
                toX = self.toElbow.x()
                minX = min(fromX,toX)
                maxX = max(fromX,toX)
                minX+=1
                maxX-=1
                y = self.fromElbow.y()
                return Path.Segment.Snapshot(y,minX,maxX)
            else:
                fromY = self.fromElbow.y()
                toY = self.toElbow.y()
                minY = min(fromY,toY)
                maxY = max(fromY,toY)
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

    def createSegmentList(self):
        elbows = self.createElbowList()
        segmentList = []
        prevElbow = None
        for elbow in elbows:
            if prevElbow:
                segment = Path.Segment()
                segment.fromElbow = prevElbow
                segment.toElbow = elbow
                if prevElbow.x()==elbow.x():
                    segment.orientation = Orientation.VERTICAL
                elif  prevElbow.y()==elbow.y():
                    segment.orientation = Orientation.HORIZONTAL
                else:
                    raise Exception("segments are neither horizontal or vertical")

                segmentList.append( segment )

            prevElbow = elbow

        return segmentList

    def draw(self,context):
        self.drawSegmentList(context,createSegmentList)

    def drawArrow(self,context,segment,isFrom):
        if isFrom:
            otherElbow = segment.toElbow
            endElbow = segment.fromElbow
        else:
            otherElbow = segment.fromElbow
            endElbow = segment.toElbow

        endX = endElbow.x()
        endY = endElbow.y()
        index = -1
        if segment.orientation == Orientation.HORIZONTAL:
            otherX = otherElbow.x()
            if endX < otherX:
                index = 0
            elif endX > otherX:
                index = 1
            #if index !=-1 and not isFrom:
            #    index = 5 - index # swap directions
        else:
            otherY = otherElbow.y()
            if endY < otherY:
                index = 2
            elif endY > otherY:
                index = 3
            #if index!=-1 and not isFrom:
            #    index = 1 - index # swap directions
        if index != -1:
            context.orChar(endX,endY,self.startArrowCharArray[index])

    def drawSegmentList(self,context,segmentList):
        first = True
        for segment in segmentList:
            direction = segment.direction()
            if first:
                self.drawArrow(context,segment,True)
                first = False
            else:
                elbow = segment.fromElbow
                context.orChar(elbow.x(),elbow.y(),self.elbowSymbol[oldDirection.value][direction.value])

            snapshot = segment.getSnapshot()
            if snapshot.fro<=snapshot.to:
                if segment.orientation==Orientation.HORIZONTAL:
                    context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to)
                else:
                    context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to)
            oldDirection = direction
        self.drawArrow(context,segment,False)


