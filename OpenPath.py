from Path import *


class OpenPath(Path):

    _noneArrowArray =     [ "╶", "╴", "╷", "╵" ]
    _linesArrowArray =    [ "<", ">", "∧", "∨" ]
    _triangleArrowArray = [ "◁", "▷", "△", "▽" ]

    def __init__(self,initialOrientation,elbowRefs):
        super().__init__(initialOrientation,elbowRefs)
        self.startArrow = Arrow.LINES
        self.endArrow = Arrow.LINES

    def createElbow(self,path,index,xRefIndex,yRefIndex):
        if index==0 or index==len(self.elbowRefs)-2:
            return OpenPath.ArrowElbow(self,path,index,xRefIndex,yRefIndex)
        else:
            return super().createElbow(path,index,xRefIndex,yRefIndex)

    def getRect(self):
        rect = Rect()
        for segment in self.segments:
            rect.unionWith(segment.getRect())
        rect.unionWith(self.segments[0].fromElbow.getRect())
        rect.unionWith(self.segments[-1].toElbow.getRect())
        return rect

    def _setArrow(self,name,value):
        if value==Arrow.NONE:
            array = OpenPath._noneArrowArray
        elif value==Arrow.LINES:
            array = OpenPath._linesArrowArray
        elif value==Arrow.TRIANGLE:
            array = OpenPath._triangleArrowArray
        setattr(self,name+"CharArray", array)

    def __setattr__(self,name,value):
        super().__setattr__(name,value)
        if name=="startArrow" or name=="endArrow":
            self._setArrow(name,value)

    def drawArrow(self,context,segment,isFrom,bold):
        if isFrom:
            otherElbow = segment.toElbow
            endElbow = segment.fromElbow
        else:
            otherElbow = segment.fromElbow
            endElbow = segment.toElbow

        endX = endElbow.getX()
        endY = endElbow.getY()
        index = -1
        if segment.orientation == Orientation.HORIZONTAL:
            otherX = otherElbow.getX()
            if endX < otherX:
                index = 0
            elif endX > otherX:
                index = 1
        else:
            otherY = otherElbow.getY()
            if endY < otherY:
                index = 2
            elif endY > otherY:
                index = 3
        if index != -1:
            if isFrom:
                array = self.startArrowCharArray
            else:
                array = self.endArrowCharArray
            context.orChar(endX,endY,array[index],bold)

    def draw(self,context,bold):
        #segmentList = self.createSegmentList(self.elbowRefs)
        first = True
        for segment in self.segments:
            direction = segment.direction()
            if first:
                self.drawArrow(context,segment,True,bold)
                first = False
            else:
                elbow = segment.fromElbow
                context.orChar(elbow.getX(),elbow.getY(),self.elbowSymbol[oldDirection.value][direction.value],bold)

            snapshot = segment.getSnapshot()
            if snapshot.fro<=snapshot.to:
                if segment.orientation==Orientation.HORIZONTAL:
                    context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to,bold)
                else:
                    context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to,bold)
            oldDirection = direction
        self.drawArrow(context,segment,False,bold)

    def isPointInPath(self,point):
        parentResult = super().isPointInPath(point)
        if parentResult:
            return True
        else:
            endElbow = self.segments[-1].toElbow
            return point.isEqual(endElbow.getX(), endElbow.getY())


    class ArrowElbow(Path.Elbow):
        def __init__(self,parent,path,index,xRef,yRef):
            super().__init__(parent,path,index,xRef,yRef)

        def connectTo(self,segment,point):
            path = self.path
            elbowRefs = path.elbowRefs

            if self.index==0:
                xIndex = 0
            else:
                xIndex = len(elbowRefs)-2
            yIndex = xIndex+1

            initVertical = path.initialOrientation==Orientation.VERTICAL
            if (xIndex==0 and initVertical) or (xIndex%2==0 and initVertical): # if my segment is vertical than swap
                temp = xIndex
                xIndex = yIndex
                yIndex = temp

            print("invoked ArrowElbow.connectTo segment="+str(segment)+" point="+str(point)+" xIndex="+str(xIndex)+" yIndex="+str(yIndex))

            if segment.orientation==Orientation.HORIZONTAL:
                xRef = VarReference(point.x)
                yRef = segment.getPosRef()
            else:
                xRef = segment.getPosRef()
                yRef = VarReference(point.y)

            elbowRefs[xIndex]= xRef
            elbowRefs[yIndex]= yRef

        def edit(self,offset):
            xRef = self.parent.elbowRefs[self.xRefIndex]
            xRef.set( xRef.get() + offset.x )
            yRef = self.parent.elbowRefs[self.yRefIndex]
            yRef.set( yRef.get() + offset.y )
