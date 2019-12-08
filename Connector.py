from Path import *


class Connector(Path):

    _noneArrowArray =     [ "╶", "╴", "╷", "╵" ]
    _linesArrowArray =    [ "<", ">", "∧", "∨" ]
    _triangleArrowArray = [ "◁", "▷", "△", "▽" ]

    def __init__(self,initialOrientation):
        Path.__init__(self,initialOrientation)
        self.startArrow = Arrow.LINES
        self.endArrow = Arrow.LINES

    def _setArrow(self,name,value):
        if value==Arrow.NONE:
            array = Connector._noneArrowArray
        elif value==Arrow.LINES:
            array = Connector._linesArrowArray
        elif value==Arrow.TRIANGLE:
            array = Connector._triangleArrowArray
        setattr(self,name+"CharArray", array)

    def __setattr__(self,name,value):
        if name=="startArrow" or name=="endArrow":
            self._setArrow(name,value)
        super().__setattr__(name,value)

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
        else:
            otherY = otherElbow.y()
            if endY < otherY:
                index = 2
            elif endY > otherY:
                index = 3
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

