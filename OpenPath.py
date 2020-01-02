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
            return OpenPath.ArrowElbow(path,index,xRefIndex,yRefIndex)
        else:
            return super().createElbow(path,index,xRefIndex,yRefIndex)

    class ArrowElbow(Path.Elbow):
        def __init__(self,path,index,xRef,yRef):
            super().__init__(path,index,xRef,yRef)

        def connectTo(self,segment,point):
            #path = segment.parent
            #if segment.orientation==Orientation.HORIZONTAL:
            #    xRef =
            #    yRef = segment.getPosRef()
            #else:
            #    xRef = segment.getPosRef()
            #    yRef =
            print("invoked ArrowElbow.connectTo segment="+str(segment)+" point="+str(point))

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

    def drawArrow(self,context,segment,isFrom):
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
            context.orChar(endX,endY,array[index])

    def drawSegmentList(self,context,segmentList):
        first = True
        for segment in segmentList:
            direction = segment.direction()
            if first:
                self.drawArrow(context,segment,True)
                first = False
            else:
                elbow = segment.fromElbow
                context.orChar(elbow.getX(),elbow.getY(),self.elbowSymbol[oldDirection.value][direction.value])

            snapshot = segment.getSnapshot()
            if snapshot.fro<=snapshot.to:
                if segment.orientation==Orientation.HORIZONTAL:
                    context.drawHorizontalLine(snapshot.pos,snapshot.fro,snapshot.to)
                else:
                    context.drawVerticalLine(snapshot.pos,snapshot.fro,snapshot.to)
            oldDirection = direction
        self.drawArrow(context,segment,False)

