from Util import *
from Model import *

class Path:

    def _fillTurnSymbols(self):
        tl = self.corners[0]
        tr = self.corners[1]
        bl = self.corners[2]
        br = self.corners[3]
        h = self.corners[4]
        v = self.corners[5]
        sp = " "
        self.turnSymbol = \
              [ [ h,tr,sp,br], \
                [bl, v,br,sp], \
                [sp,tl, h,bl], \
                [tl,sp,tr, v] ]

    def __init__(self,initialOrientation):
        self.turnRefs = []
        self.initialOrientation = initialOrientation
        self.corners = [ "┌", "┐", "└", "┘", "─", "│" ]
        self._fillTurnSymbols()

    def appendTurnRef(self,turnRef):
        self.turnRefs.append(turnRef)

    class Turn:
        def __init__(self,xRef,yRef):
            self.xRef = xRef
            self.yRef = yRef
            self.char = None

        def x(self):
            return self.xRef.get()

        def y(self):
            return self.yRef.get()


    def createTurnList(self):
        turnList = []
        horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
        first = True
        prevDirection = None
        xPrev = None
        yPrev = None
        prevTurn = None
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
                    if xPrev==None or xPrev > x:
                        direction = None
                    elif xPrev < x:
                        direction = Direction.RIGHT
                    else:
                        direction = Direction.LEFT
                else:
                    if yPrev==None or yPrev > y:
                        direction = None
                    elif yPrev < y:
                        direction = Direction.DOWN
                    else:
                        direction = Direction.UP

                #print("prevDirection="+str(prevDirection)+ 
                if prevDirection!=None and direction!=None:
                    prevTurn.char = self.turnSymbol[prevDirection.value][direction.value]
                prevDirection = direction
                prevTurn = turnRef

            if horizontalOrienation:
                xPrev = x
            else:
                yPrev = y
            horizontalOrienation = not horizontalOrienation

        return turnList


    def draw(self,context):

        for turn in self.createTurnList():
            context.orChar(turn.x().turn.y(),turn.char)

        #horizontalOrienation = self.initialOrientation==Orientation.HORIZONTAL
        #if horizontalOrienation:
        #    x=
        #    
        #x,y = self.drawConnector(context,fromConnection)
        #endX,endY = self.drawConnector(context,toConnection)

        #controlPoints = self.element.controlPoints.copy()
        #if isHorizontal(toConnection.side):
        #    controlPoints.append(endY)
        #    controlPoints.append(endX)
        #else:
        #    controlPoints.append(endX)
        #    controlPoints.append(endY)

        #horizontalOrienation = isHorizontal(fromConnection.side)
        #if fromConnection.side==Side.RIGHT:
        #    direction = 0
        #elif fromConnection.side==Side.BOTTOM:
        #    direction = 1
        #elif fromConnection.side==Side.LEFT:
        #    direction = 2
        #elif fromConnection.side==Side.TOP:
        #    direction = 3

        #for controlPoint in controlPoints:
        #    print("x="+str(x)+" y="+str(y)+" controlPoint="+str(controlPoint))
        #    if horizontalOrienation:
        #        if controlPoint>x:
        #            newDirection = 0
        #        else:
        #            newDirection = 2
        #        context.drawHorizontalLine(y,x,controlPoint,False,isBold)
        #        nextX=controlPoint
        #        nextY=y
        #    else:
        #        if controlPoint>y:
        #            newDirection = 1
        #        else:
        #            newDirection = 3
        #        context.drawVerticalLine(x,y,controlPoint,False,isBold)
        #        nextX=x
        #        nextY=controlPoint
        #    context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])
        #    x=nextX
        #    y=nextY
        #    print("oldDirection="+str(direction)+" newDirection="+str(newDirection))
        #    direction = newDirection
        #    horizontalOrienation = 1 - horizontalOrienation

        #context.addString(x,y,ConnectorComponent.turnSymbol[direction][newDirection])


    #def draw(self,context):
    #    horizontalOrientation = elementContainer.startOrientation==Orientation.HORIZONTAL

    #
    #    if horizontalOrientation:
    #        refs.append( AttrReference(element.startPoint,"x") )
    #        refs.append( AttrReference(element.startPoint,"y") )
    #    else:
    #        refs.append( AttrReference(element.startPoint,"y") )
    #        refs.append( AttrReference(element.startPoint,"x") )

    #        context.drawHorizontalLine(

    #    for index in range(len(element.turns)):
    #        refs.append( ArrayElementReference(element.turns,index) )

    #    self.createSegments(refs,horizontalOrientation)
    #    self.createElbows(refs)

    def createSegments(self,refs,startHorizontal):
        directionMap = { True:Orientation.HORIZONTAL, False:Orientation.VERTICAL }
        for index in range(len(refs)-2):
            self.segments.append( PathComponent.Segment(self,refs[index],refs[index+1],refs[index+2],directionMap[startHorizontal]) )
            startHorizontal = 1 - startHorizontal


