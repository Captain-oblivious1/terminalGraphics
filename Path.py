from Util import *
from Model import *
from Components import *

class Path:

    def setCorners(self,corners):
        tl = corners[0]
        tr = corners[1]
        bl = corners[2]
        br = corners[3]
        h =  corners[4]
        v =  corners[5]
        sp = " "
        self.turnSymbol = \
              [ [ h,tr,sp,br], \
                [bl, v,br,sp], \
                [sp,tl, h,bl], \
                [tl,sp,tr, v] ]

    def __init__(self,initialOrientation):
        self.turnRefs = []
        self.initialOrientation = initialOrientation
        self.setCorners( [ "┌", "┐", "└", "┘", "─", "│" ] )

    def appendTurnRef(self,turnRef):
        self.turnRefs.append(turnRef)

    class Turn:
        def __init__(self,xRef,yRef):
            self.xRef = xRef
            self.yRef = yRef
            self.char = "#"

        def x(self):
            return self.xRef.get()

        def y(self):
            return self.yRef.get()

        def __str__(self):
            return "Turn{x="+str(self.xRef.get())+",y="+str(self.yRef.get())+",char='"+self.char+"'}"

    def createTurnList(self):
        turnList = []
        horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
        first = True
        prevDirection = None
        xPrev = None
        yPrev = None
        prevTurn = None
        x=None
        y=None
        for turnRef in self.turnRefs:

            if horizontalOrienation:
                xRef = turnRef
                x = xRef.get()
            else:
                yRef = turnRef
                y = yRef.get()

            if first:
                first = False
            else:
                turn = Path.Turn(xRef,yRef)
                turnList.append(turn)
                if horizontalOrienation:
                    if xPrev==None or xPrev==x:
                        direction = None
                    elif xPrev < x:
                        direction = Direction.RIGHT
                    else:
                        direction = Direction.LEFT
                else:
                    if yPrev==None or yPrev==y:
                        direction = None
                    elif yPrev < y:
                        direction = Direction.DOWN
                    else:
                        direction = Direction.UP

                if prevDirection!=None and direction!=None:
                    prevTurn.char = self.turnSymbol[prevDirection.value][direction.value]
                prevDirection = direction
                prevTurn = turn

            if horizontalOrienation:
                xPrev = x
            else:
                yPrev = y
            horizontalOrienation = not horizontalOrienation

        return turnList

    class Segment:
        def __init__(self):
            self.fromTurn = None
            self.toTurn = None
            self.orientation = None

        class Snapshot:
            def __init__(self,pos,fro,to):
                self.pos = pos
                self.fro = fro
                self.to = to

        def getPosRef(self):
            if self.orientation==Orientation.HORIZONTAL:
                return self.fromTurn.yRef
            else:
                return self.fromTurn.xRef

        def getSnapshot(self):
            if self.orientation==Orientation.HORIZONTAL:
                fromX = self.fromTurn.x()
                toX = self.toTurn.x()
                if fromX<toX:
                    fromX+=1
                    toX-=1
                elif fromX>toX:
                    fromX-=1
                    toX+=1
                y = self.fromTurn.y()
                return Path.Segment.Snapshot(y,fromX,toX)
            else:
                fromY = self.fromTurn.y()
                toY = self.toTurn.y()
                if fromY<toY:
                    fromY+=1
                    toY-=1
                elif fromY>toY:
                    fromY-=1
                    toY+=1
                x = self.fromTurn.x()
                return Path.Segment.Snapshot(x,fromY,toY)

        def getRect(self):
            snapshot = self.getSnapshot()
            if self.orientation==Orientation.HORIZONTAL:
                return Rect(snapshot.fro,snapshot.pos,snapshot.to,snapshot.pos)
            else:
                return Rect(snapshot.pos,snapshot.fro,snapshot.pos,snapshot.to)

    def createSegmentList(self):
        turns = self.createTurnList()
        segmentList = []
        prevTurn = None
        for turn in turns:
            if prevTurn:
                segment = Path.Segment()
                segment.fromTurn = prevTurn
                segment.toTurn = turn
                if prevTurn.x()==turn.x():
                    segment.orientation = Orientation.VERTICAL
                elif  prevTurn.y()==turn.y():
                    segment.orientation = Orientation.HORIZONTAL
                else:
                    raise Exception("segments are neither horizontal or vertical")

                segmentList.append( segment )

            prevTurn = turn

        return segmentList



    def draw(self,context):

        first = True
        for segment in self.createSegmentList():
            snapshot = segment.getSnapshot()
            if first:
                first = False
            else:
                turn = segment.fromTurn
                context.orChar(turn.x(),turn.y(),turn.char)
            if segment.orientation==Orientation.HORIZONTAL:
                context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to)
            else:
                context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to)


